import pandas as pd


class Transformer:

    @staticmethod
    def to_datetime(df: pd.DataFrame, colname: str) -> pd.DataFrame:
        """
        Converts a column in the DataFrame to datetime format.

        Parameters:
        df (pd.DataFrame): The DataFrame that contains the data.
        colname (str): The name of the column to be converted to datetime format.

        Returns:
        pd.DataFrame: The DataFrame with the specified column converted to datetime.

        Raises:
        ValueError: If the input is not a DataFrame.
        Exception: Captures any other exceptions that may occur during conversion.
        """
        try:
            if isinstance(df, pd.DataFrame):
                df[colname] = pd.to_datetime(df[colname])
                return df
            else:
                raise ValueError("The input data is not a DataFrame")
        except Exception as e:
            print(f"Other exception {e}")
            return f"Other exception {e}"

    @staticmethod
    def drop_negative(df: pd.DataFrame, colname: str) -> pd.DataFrame:
        """
        Removes rows where the value in the specified column is negative.

        Parameters:
        df (pd.DataFrame): The DataFrame from which to remove rows.
        colname (str): The column name where negative values are checked.

        Returns:
        pd.DataFrame: The DataFrame with negative values removed from the specified column.

        Raises:
        ValueError: If the input is not a DataFrame.
        Exception: Captures any other exceptions that may occur during filtering.
        """
        try:
            if isinstance(df, pd.DataFrame):
                df = df[df[colname] >= 0]
                return df
            else:
                raise ValueError("The input data is not a DataFrame")
        except Exception as e:
            print(f"Other exception {e}")
            return f"Other exception {e}"

    @staticmethod
    def drop_constants(df: pd.DataFrame, col_array: list) -> pd.DataFrame:
        """
        Drops the specified columns from the DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame from which columns are to be dropped.
        col_array (list): A list of column names to be dropped.

        Returns:
        pd.DataFrame: The DataFrame with specified columns removed.

        Raises:
        ValueError: If the input is not a DataFrame.
        Exception: Captures any other exceptions that may occur during the dropping process.
        """
        try:
            if isinstance(df, pd.DataFrame):
                df = df.drop(col_array, axis=1)
                return df
            else:
                raise ValueError("The input data is not a DataFrame")
        except Exception as e:
            print(f"Other exception {e}")
            return f"Other exception {e}"
