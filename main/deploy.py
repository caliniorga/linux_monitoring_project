import sys
import os
import numpy as np
import pickle
from datetime import datetime
import train_constants
from sklearn.ensemble import IsolationForest
from typing import Any, Tuple


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


def preprocess_data(data: Any) -> Tuple[np.ndarray, np.ndarray, Any]:
    """
    Processes data to calculate thresholds, define anomalies, and extract features,
    then splits the data into training and unused subsets.

    Args:
    data (Any): Data returned from the fetch_data function.

    Returns:
    Tuple[np.ndarray, np.ndarray, Any]: Training features, labels, and the processed data.
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
    return X, y, data


def load_model(filename: str = "model.pkl") -> IsolationForest:
    """
    Loads the trained model from disk using pickle.

    Args:
    filename (str): The filename to load the model from.

    Returns:
    IsolationForest: The loaded model.
    """
    with open(filename, "rb") as file:
        model = pickle.load(file)
    return model


def send_notifications(anomalies: Any, num_rows: int) -> None:
    """
    Sends notifications for a specified number of latest detected anomalies.

    Args:
    anomalies (Any): Data containing the detected anomalies.
    num_rows (int): The number of latest rows with anomalies to send notifications for.
    """
    from notification import Notification

    if not anomalies.empty:
        host = "smtp.gmail.com"
        port = 587
        from_addr = "linuxmonitoringproject@gmail.com"
        password = "zgvc cxwi fbfb cczq"
        to_addr = "linuxmonitoringproject@gmail.com"
        table = "linux_records"
        notification = Notification(
            host, password, from_addr, to_addr, table, port=port
        )

        latest_anomalies = anomalies.tail(num_rows)

        for index, row in latest_anomalies.iterrows():
            date = row["record_timestamp"].strftime("%B %d, %Y %H:%M:%S")
            column_values = row.to_dict()
            formatted_message = notification.format_as_table(column_values)
            notification.send_error_prediction_email(
                "Anomaly Detected", date, formatted_message
            )
            if index >= 1000:
                break


def main() -> None:
    """
    Main function to execute the data fetching, preprocessing, anomaly detection,
    and notification workflow.
    """
    setup_project_path(train_constants.HELPER_PATH)
    data = fetch_data()
    X, y, processed_data = preprocess_data(data)

    model = load_model()
    predictions = model.predict(X)

    processed_data["anomaly"] = predictions
    anomalies = processed_data[processed_data["anomaly"] == -1]

    num_rows = 400000

    send_notifications(anomalies, num_rows)


if __name__ == "__main__":
    main()
