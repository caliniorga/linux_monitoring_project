import configparser
import sys
import os

import psycopg2
import pandas as pd


class Connect:
    """Class used to connect to PostgreSQL and import the table as a DataFrame."""

    def __init__(self, sql_query: str, config_path: str, which_database: str) -> None:
        """
        Initialize the connection settings.

        Args:
            sql_query (str): SQL query to be executed.
            config_path (str): Path to the configuration file.
            which_database (str): Section name in the configuration file to retrieve database settings.
        """
        self.sql_query = sql_query
        self.config_path = config_path
        self.which_database = which_database

    def read_config(self) -> tuple:
        """
        Reads the database configuration from a file and returns connection details.

        Returns:
            tuple: A tuple containing host, user, password, dbname, and port as strings if successful, or a message string if an exception occurs.

        Raises:
            SystemExit: If the configuration file does not exist.
        """
        try:
            if os.path.exists(self.config_path):
                parser = configparser.ConfigParser()
            else:
                print("Config not found!")
                sys.exit(1)
            parser.read(self.config_path)
            host = parser.get(self.which_database, "host")
            user = parser.get(self.which_database, "user")
            password = parser.get(self.which_database, "password")
            dbname = parser.get(self.which_database, "dbname")
            port = parser.get(self.which_database, "port")
            return host, user, password, dbname, port
        except OSError as e:
            return f"Exception error: {e}"

    def dbconnector(self) -> pd.DataFrame:
        """
        Connects to the PostgreSQL database using the settings from read_config and executes the SQL query.

        Returns:
            pd.DataFrame: The result of the SQL query as a DataFrame.

        Raises:
            Exception: If there is a database connection error or other exceptions occur.
        """
        try:
            host, user, password, dbname, port = self.read_config()
            conn = psycopg2.connect(
                dbname=dbname, host=host, port=int(port), user=user, password=password
            )
            print(f"Successfully connected to the database on host: {host}")
            df = pd.read_sql(sql=self.sql_query, con=conn)

            if len(df) == 0:
                print("Data has not been landed.")
            return df
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            raise
        except Exception as e:
            print(f"Other exception error: {e}")
            raise
