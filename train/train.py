import sys
import os
import numpy as np
import pickle
import train_constants
from sklearn.ensemble import IsolationForest
from typing import Tuple, Any, Dict


def setup_project_path(helper_path: str) -> None:
    """
    Adds the specified path to sys.path to enable relative imports.

    Args:
    helper_path (str): The relative path to the helper directory in the project.
    """
    project_root = os.path.abspath(os.path.join("..", helper_path))
    if project_root not in sys.path:
        sys.path.append(project_root)


def fetch_data() -> Any:
    """
    Connects to the database and fetches data, processes it by applying various transformations
    such as converting timestamps, dropping negative and constant columns, and calculating differences.

    Returns:
    Any: The processed data ready for further feature extraction and transformation.
    """
    import dbconnector, etl, feature_extractor

    db = dbconnector.Connect(
        train_constants.SQL_QUERY,
        train_constants.CONFIG_PATH,
        train_constants.DATABASE,
    )
    data = db.dbconnector()
    data = etl.Transformer.to_datetime(data, "record_timestamp")
    data = etl.Transformer.drop_negative(data, "idle")
    data = etl.Transformer.drop_constants(data, train_constants.CONST_COLS)
    data = feature_extractor.Transformer.get_col_diff(data, "sys")
    return data


def preprocess_data(data: Any) -> Tuple[np.ndarray, np.ndarray]:
    """
    Processes data to calculate thresholds, define anomalies, and extract features,
    then splits the data into training and unused subsets.

    Args:
    data (Any): Data returned from the fetch_data function.

    Returns:
    Tuple[np.ndarray, np.ndarray]: Training features and labels.
    """
    import feature_extractor

    threshold = feature_extractor.Transformer.calculate_threshold(data, "sys_diff")
    data = feature_extractor.Transformer.define_anomaly(data, "sys_diff", threshold)
    data = feature_extractor.Transformer.get_diff_threshold_ratio(
        data, "sys_diff", threshold
    )
    data = feature_extractor.Transformer.get_diff_mean_ratio(
        data, "sys_diff", data["sys_diff"].mean()
    )

    X = data[train_constants.FEATURES]
    y = data["anomaly"]
    X_train, _ = np.split(X, [int(0.67 * len(X))])
    return X_train, y


def train_model(X_train: np.ndarray, y: np.ndarray) -> IsolationForest:
    """
    Trains an Isolation Forest model with specific parameters on the provided training data.

    Args:
    X_train (np.ndarray): The training features.
    y (np.ndarray): The training labels.

    Returns:
    IsolationForest: The trained model.
    """
    params = {
        "n_estimators": train_constants.N_ESTIMATORS,
        "max_samples": train_constants.MAX_SAMPLES,
        "contamination": float(np.sum(y == -1) / len(y)),
        "random_state": train_constants.RANDOM_STATE,
    }
    model = IsolationForest(**params)
    model.fit(X_train)
    return model


def save_model(model: IsolationForest, filename: str = "model.pkl") -> None:
    """
    Saves the trained model to disk using pickle.

    Args:
    model (IsolationForest): The trained model to be saved.
    filename (str): The filename to save the model under.
    """
    with open(filename, "wb") as file:
        pickle.dump(model, file)


def main() -> None:
    """
    Main function to execute the data fetching, preprocessing, model training, and saving workflow.
    """
    setup_project_path(train_constants.HELPER_PATH)
    data = fetch_data()
    X_train, y = preprocess_data(data)
    model = train_model(X_train, y)
    save_model(model)


if __name__ == "__main__":
    main()
