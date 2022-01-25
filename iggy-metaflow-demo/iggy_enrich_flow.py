from iggy_metaflow_base import IggyFlow, LoadedDataset
from metaflow import FlowSpec, step, Parameter
from collections import namedtuple


class IggyEnrichFlow(FlowSpec, IggyFlow):
    @step
    def start(self):
        # Load Data
        self.file_prefix = "enrich"
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
        ) = self.dataset[0]
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
        self.next(self.feature_selection)

    @step
    def feature_selection(self):
        (
            X_train,
            y_train,
            X_val,
            y_val,
            X_test,
            y_test,
        ) = self.dataset[0]

        # Feature Selection
        (X_train, X_val, X_test), selected_features = self.select_features(
            X_train, y_train, X_val, y_val, X_test, y_test
        )
        self.selected_features = selected_features
        self.dataset = LoadedDataset(
            (
                X_train,
                y_train,
                X_val,
                y_val,
                X_test,
                y_test,
            ),
            self.dataset[1],
        )
        self.next(self.train_model)

    @step
    def train_model(self):
        import pandas as pd
        from metaflow import S3

        (
            X_train,
            y_train,
            X_val,
            y_val,
            X_test,
            y_test,
        ) = self.dataset.data
        scaled_features = self.dataset.scaled_features
        # Tain model
        model = self.train(X_train, y_train, X_val, y_val)

        # Eval Model
        mean, std = scaled_features[self.label_col]
        self.eval_result = self.eval(model, X_test, y_test, mean, std)
        print(f"Test result: {self.eval_result}")

        # Get feature importances
        feature_impts = dict(zip(self.selected_features, model.feature_importances_))
        fw = pd.DataFrame.from_dict({self.file_prefix: feature_impts}, orient="index")
        fw = fw.fillna(0)
        fw.reset_index(inplace=True)
        csv_path = "feature_importances/feature_importances_%s.csv" % self.file_prefix
        fw.to_csv(csv_path, index=False)
        self.results = fw
        self.next(self.end)

    @step
    def end(self):
        print("Done Computation")


if __name__ == "__main__":
    IggyEnrichFlow()
