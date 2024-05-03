import pandas as pd
import numpy as np


class Transformer:

    @staticmethod
    def get_col_diff(df: pd.DataFrame, colname: str) -> pd.DataFrame:
        """
        Calculates the difference between consecutive entries in the specified column
        and fills missing values with 0.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        colname (str): The column name for which the difference is to be calculated.

        Returns:
        pd.DataFrame: The DataFrame with the difference column added.

        Raises:
        ValueError: If the input is not a DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data is not a DataFrame")
        df[colname + "_diff"] = df[colname].diff().fillna(0)
        return df

    @staticmethod
    def calculate_threshold(df: pd.DataFrame, diff_colname: str) -> float:
        """
        Calculates the anomaly threshold as the mean of the difference column plus two standard deviations.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        diff_colname (str): The column name of the difference data.

        Returns:
        float: The calculated threshold.

        Raises:
        ValueError: If the input is not a DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data is not a DataFrame")
        mean_diff = df[diff_colname].mean()
        std_diff = df[diff_colname].std()
        return mean_diff + 2 * std_diff

    @staticmethod
    def define_anomaly(
        df: pd.DataFrame, colname: str, threshold: float
    ) -> pd.DataFrame:
        """
        Identifies anomalies in a column based on a threshold. Anomalies are marked as -1, others as 1.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        colname (str): The column name to check for anomalies.
        threshold (float): The threshold value above which an entry is considered an anomaly.

        Returns:
        pd.DataFrame: The DataFrame with the anomaly column added.

        Raises:
        ValueError: If the input is not a DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data is not a DataFrame")
        df["anomaly"] = np.where(df[colname] > threshold, -1, 1)
        return df

    @staticmethod
    def get_diff_threshold_ratio(
        df: pd.DataFrame, col_diff_name: str, threshold: float
    ) -> pd.DataFrame:
        """
        Calculates the ratio of the difference column to a threshold.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        col_diff_name (str): The column name of the difference data.
        threshold (float): The threshold value used for the ratio.

        Returns:
        pd.DataFrame: The DataFrame with the threshold ratio column added.

        Raises:
        ValueError: If the input is not a DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data is not a DataFrame")
        df[col_diff_name + "_threshold_ratio"] = df[col_diff_name] / threshold
        return df

    @staticmethod
    def get_diff_mean_ratio(
        df: pd.DataFrame, col_diff_name: str, mean_diff: float
    ) -> pd.DataFrame:
        """
        Calculates the ratio of the difference column to the mean of the differences.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        col_diff_name (str): The column name of the difference data.
        mean_diff (float): The mean value of the differences used for the ratio.

        Returns:
        pd.DataFrame: The DataFrame with the mean ratio column added.

        Raises:
        ValueError: If the input is not a DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data is not a DataFrame")
        df[col_diff_name + "_mean_ratio"] = df[col_diff_name] / mean_diff
        return df
