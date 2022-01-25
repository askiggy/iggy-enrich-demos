from metaflow import JSONType, Parameter
import json
from collections import namedtuple

LoadedDataset = namedtuple("LoadedDataset", "data scaled_features")

IGGY_DATA_BASE_LOCATION = "../iggy-data"
BENCHMARK_DATA_LOCATION = "./data/benchmark/iggy_re_salesprice_pinellas_20211203.csv"

DEFAULT_IGGY_PKG_CONFIG = {
    "iggy_version_id": "20211110214810",
    "crosswalk_prefix": "fl_pinellas_quadkeys",
    "iggy_prefix": "fl_pinellas_quadkeys",
}

IGGY_FEATURES = [
    "area_sqkm_qk_isochrone_walk_10m",
    "population_qk_isochrone_walk_10m",
    "poi_count_per_capita_qk_isochrone_walk_10m",
    "poi_count_qk_isochrone_walk_10m",
    "poi_is_transportation_count_qk_isochrone_walk_10m",
    "poi_is_restaurant_count_qk_isochrone_walk_10m",
    "poi_is_social_and_community_services_count_qk_isochrone_walk_10m",
    "poi_is_religious_organization_count_per_capita_qk_isochrone_walk_10m",
    "park_intersecting_area_in_sqkm_qk_isochrone_walk_10m",
    "coast_intersecting_length_in_km_qk_isochrone_walk_10m",
    "coast_intersects_cbg",
    "acs_pop_employment_status_in_labor_force_civilian_unemployed_cbg",
    "acs_pct_households_with_no_internet_access_cbg",
    "acs_median_rent_cbg",
    "acs_median_year_structure_built_cbg",
    "acs_median_age_cbg",
]


class IggyFlow:
    label_col = "log_price_per_sqft"

    location_cols = ["latitude", "longitude"]

    model_dim = 50

    iggy_config = Parameter(
        "iggy-config",
        type=JSONType,
        help="configuration JSON object",
        default=json.dumps(DEFAULT_IGGY_PKG_CONFIG),
    )

    iggy_features = Parameter(
        "iggy-features",
        type=JSONType,
        help="selected Iggy features",
        default=json.dumps(IGGY_FEATURES),
    )

    s3_data_base_path = Parameter(
        "base-data-path",
        default=IGGY_DATA_BASE_LOCATION,
        help="S3 path to Iggy config `base_loc`",
    )

    benchmark_data_path = Parameter(
        "benchmark-data-path",
        help="S3 path to benchmark dataset",
        default=BENCHMARK_DATA_LOCATION,
    )

    def load_data(self, drop_cols=True):
        # load dataset
        from utils import load_dataset

        data, scaled_features = load_dataset(
            self.benchmark_data_path,
            self.label_col,
            "split",
            debug=False,
            location_cols=self.location_cols,
        )
        (
            X_train,
            y_train,
            X_val,
            y_val,
            X_test,
            y_test,
        ) = data
        if drop_cols:
            X_train.drop(self.location_cols, axis=1, inplace=True)
            X_val.drop(self.location_cols, axis=1, inplace=True)
            X_test.drop(self.location_cols, axis=1, inplace=True)
        return (
            (
                X_train,
                y_train,
                X_val,
                y_val,
                X_test,
                y_test,
            ),
            scaled_features,
        )

    def select_features(self, X_train, y_train, X_val, y_val, X_test, y_test):
        # feature selection
        from utils import feature_selection

        (X_train, X_val, X_test), selected_features = feature_selection(
            [X_train, X_val, X_test], y_train, self.model_dim
        )
        return (X_train, X_val, X_test), selected_features

    def train(self, X_train, y_train, X_val, y_val):
        from utils import train

        return train(X_train, y_train, X_val, y_val)

    def iggy_enrich(self, X_train, y_train, X_val, y_val, X_test, y_test):
        from iggyenrich.iggy_enrich import IggyEnrich
        from iggyenrich.iggy_data_package import LocalIggyDataPackage
        from utils import impute_missing_values, scale_continuous_values

        config = dict(self.iggy_config)
        config["base_loc"] = self.s3_data_base_path
        iggy = IggyEnrich(iggy_package=LocalIggyDataPackage(**config))
        iggy.load(features=IGGY_FEATURES)

        X_train = iggy.enrich_df(X_train)
        X_train.drop(self.location_cols, axis=1, inplace=True)
        X_train, scaled_enriched_features = scale_continuous_values(
            impute_missing_values(X_train)
        )

        X_val = iggy.enrich_df(X_val)
        X_val.drop(self.location_cols, axis=1, inplace=True)
        X_val, __ = scale_continuous_values(
            impute_missing_values(X_val), scaled_features=scaled_enriched_features
        )

        X_test = iggy.enrich_df(X_test)
        X_test.drop(self.location_cols, axis=1, inplace=True)
        X_test, __ = scale_continuous_values(
            impute_missing_values(X_test), scaled_features=scaled_enriched_features
        )

        return X_train, X_val, X_test

    def eval(self, model, X_test, y_test, mean, std):
        from utils import eval

        return eval(model, X_test, y_test, mean, std)

    def segment_df(self, x, y, col):
        from utils import segment_df

        return segment_df(x, y, col)
