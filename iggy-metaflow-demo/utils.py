import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from sklearn.impute import KNNImputer
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.ensemble import RandomForestRegressor


pd.options.mode.chained_assignment = None


def scale_continuous_values(
    df: pd.DataFrame,
    n_sample: int = 2000,
    ignore_cols: List[str] = [],
    scaled_features: Dict = {},
) -> Tuple[pd.DataFrame, Dict]:
    continuous_cols = df.columns[~df.head(n_sample).isin([0, 1]).all()]
    for col in continuous_cols:
        if col == "geometry" or col in ignore_cols:
            continue
        mean, std = scaled_features.get(col, [df[col].mean(), df[col].std()])
        scaled_features[col] = [mean, std]
        df.loc[:, col] = (df[col] - mean) / std
    return df, scaled_features


def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    imputer = KNNImputer(n_neighbors=3)
    df.loc[:, :] = imputer.fit_transform(df)
    return df


def segment_df(df_X: pd.DataFrame, df_y: pd.Series, column_prefix: str) -> Dict:
    column_selectors = [c for c in df_X.columns if c.startswith(column_prefix)]
    dfs = {}
    for col in column_selectors:
        data_key = col.replace(column_prefix, "")
        df_X_seg = df_X.loc[df_X[col] == 1]
        df_y_seg = df_y.loc[df_X_seg.index]
        df_X_seg.drop(column_selectors, axis=1, inplace=True)
        dfs[data_key] = [df_X_seg, df_y_seg]
    return dfs


def feature_selection(
    dfs: List[pd.DataFrame], y: pd.Series, model_dim: int
) -> Tuple[Tuple[pd.DataFrame], Tuple[str]]:
    """Select best features using first df in `dfs` and `y` as training, and return
    transformed features from all dfs
    """
    feature_selector = SelectKBest(mutual_info_regression, k=model_dim)
    feature_selector.fit(dfs[0], y)
    feature_names = feature_selector.get_feature_names_out(dfs[0].columns)
    transformed_dfs = [
        pd.DataFrame(feature_selector.transform(df), columns=feature_names)
        for df in dfs
    ]
    return tuple(transformed_dfs), feature_names


def train(X_train, y_train, X_val, y_val) -> RandomForestRegressor:
    """Train simple RandomForest model"""
    maxdepths = np.linspace(2, 20, 10)
    best_val = 1e6
    best_depth = -1
    best_model = None
    for md in maxdepths:
        model = RandomForestRegressor(random_state=123, max_depth=md)
        model.fit(X_train, y_train)
        y_hat = model.predict(X_val)
        val_mse = np.mean((y_val - y_hat) ** 2)
        print(f"TRAINING RESULT: val_loss={val_mse} (max_depth={md})")
        if val_mse < best_val:
            best_val = val_mse
            best_depth = md
            best_model = model
    print(f"BEST TRAINING RESULT: val_loss={best_val} (max_depth={best_depth})")
    return best_model


def eval(
    model: RandomForestRegressor,
    X_test: np.array,
    y_test: np.array,
    scaled_mean: Optional[float] = None,
    scaled_std: Optional[float] = None,
) -> Dict:
    """Evaluate performance of model on test data"""
    y_hat = model.predict(X_test)
    test_mse = np.mean((y_hat - y_test) ** 2)
    result = {"test_loss": test_mse}
    # blog note: not really necessary...we could remove this for brevity
    if scaled_mean:
        y_actuals = y_test * scaled_std + scaled_mean
        y_preds = y_hat * scaled_std + scaled_mean
        result["test_unscaled_mae"] = np.abs(y_preds - y_actuals).mean()

    return result


def load_dataset(
    file_path: str,
    label_col: str,
    split_col: str,
    index_col: str = "strap",
    location_cols: Tuple[str] = ["longitude", "latitude"],
    debug: bool = False,
) -> Tuple[Tuple[pd.DataFrame], Dict]:
    """Load base sales price prediction dataset"""
    # load file
    print(f"Loading benchmark data from {file_path}...")
    df = pd.read_csv(file_path)
    df[index_col] = df[index_col].astype(str)
    df = df.set_index(index_col)
    if debug:
        df = df.head(5000)
    print(f"Loaded {df.shape[0]} lines")

    # split
    X_train = df.loc[df[split_col] == "TRAIN"]
    X_train.drop([split_col], axis=1, inplace=True)
    X_val = df.loc[df[split_col] == "VALIDATE"]
    X_val.drop([split_col], axis=1, inplace=True)
    X_test = df.loc[df[split_col] == "TEST"]
    X_test.drop([split_col], axis=1, inplace=True)

    # scale continuous features
    X_train, scaled_features = scale_continuous_values(
        X_train, ignore_cols=location_cols
    )
    X_val, scaled_features = scale_continuous_values(
        X_val, ignore_cols=location_cols, scaled_features=scaled_features
    )
    X_test, scaled_features = scale_continuous_values(
        X_test, ignore_cols=location_cols, scaled_features=scaled_features
    )

    # separate x/y
    y_train = X_train[label_col]
    X_train.drop([label_col], axis=1, inplace=True)
    y_val = X_val[label_col]
    X_val.drop([label_col], axis=1, inplace=True)
    y_test = X_test[label_col]
    X_test.drop([label_col], axis=1, inplace=True)

    return (
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test,
    ), scaled_features
