from iggy_metaflow_base import IggyFlow, LoadedDataset
from metaflow import FlowSpec, step, catch


class IggyPerDistrictFlow(FlowSpec, IggyFlow):
    @step
    def start(self):
        import pandas as pd
        from metaflow import S3

        # Load Data
        data, scaled_features = self.load_data(drop_cols=False)
        self.dataset = LoadedDataset(data, scaled_features)
        self.next(self.enrich)

    @step
    def enrich(self):
        (
            X_train,
            y_train,
            X_val,
            y_val,
            X_test,
            y_test,
        ) = self.dataset.data

        # Run Iggy Feature Enrichment
        X_train, X_val, X_test = self.iggy_enrich(
            X_train, y_train, X_val, y_val, X_test, y_test
        )
        self.dataset = LoadedDataset(
            (
                X_train,
                y_train,
                X_val,
                y_val,
                X_test,
                y_test,
            ),
            self.dataset.scaled_features,
        )
        self.next(self.segment)

    @step
    def segment(self):
        (
            X_train,
            y_train,
            X_val,
            y_val,
            X_test,
            y_test,
        ) = self.dataset.data
        # Extract features according to districts
        tax_col = "current_tax_district_dscr_"
        self.train_data = self.segment_df(X_train, y_train, tax_col)
        self.val_data = self.segment_df(X_val, y_val, tax_col)
        self.test_data = self.segment_df(X_test, y_test, tax_col)
        self.keep_districts = [
            k for k, v in self.train_data.items() if v[0].shape[0] >= 850
        ]
        self.scaled_features = self.dataset.scaled_features
        self.next(self.feature_selection_and_train_model, foreach="keep_districts")

    @catch(var="exception")
    @step
    def feature_selection_and_train_model(self):
        # Train Many Models

        self.exception = None
        tax_dst, self.tax_district = self.input, self.input

        X_train, y_train = self.train_data[tax_dst]
        X_val, y_val = self.val_data[tax_dst]
        X_test, y_test = self.test_data[tax_dst]

        # feature selection
        (X_train, X_val, X_test), selected_features = self.select_features(
            X_train, y_train, X_val, y_val, X_test, y_test
        )

        # train model
        self.model = self.train(X_train, y_train, X_val, y_val)

        # eval
        mean, std = self.scaled_features[self.label_col]
        result = self.eval(self.model, X_test, y_test, mean, std)
        print(f"** Results for tax district {tax_dst} **")
        print(result)

        # get feature importances
        feature_impts = dict(zip(selected_features, self.model.feature_importances_))
        self.feature_importance = feature_impts
        self.next(self.join)

    @step
    def join(self, inputs):
        import pandas as pd
        from metaflow import S3

        feature_impt_by_tax = {}
        # Collecting all results at once place.
        for inp in inputs:
            # If there was an exception don't write anything.
            if inp.exception:
                continue
            feature_impt_by_tax[inp.tax_district] = inp.feature_importance
        fw = pd.DataFrame.from_dict(feature_impt_by_tax, orient="index")
        fw = fw.fillna(0)
        fw.reset_index(inplace=True)
        csv_path = "feature_importances/feature_importances_perdistrict.csv"
        fw.to_csv(csv_path, index=False)
        self.results = fw
        self.next(self.end)

    @step
    def end(self):
        print("Done Computation")


if __name__ == "__main__":
    IggyPerDistrictFlow()
