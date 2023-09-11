from datetime import datetime, timezone
from loguru import logger
import pandas as pd
from xdg_base_dirs import xdg_data_home
import sqlite3 as sql
import os


class Database:
    def __init__(self):
        self.database_file = xdg_data_home() / "open_tab_tracker.db"
        self.create_db_and_datatable_if_not_exists()

    def create_db_and_datatable_if_not_exists(self):
        conn = sql.connect(self.database_file)
        logger.info(f"Database created at {self.database_file}")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS tab_count (datetime TEXT, firefox_tab_count INTEGER)"
        )
        conn.commit()

    def write_to_database(self, firefox_tab_count: int):
        """Write the tab counts to the database, along with the current time in UTC"""
        utc_current_time = datetime.now(tz=timezone.utc)
        conn = sql.connect(self.database_file)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tab_count ('datetime', 'firefox_tab_count') VALUES (?, ?)",
            (utc_current_time, firefox_tab_count),
        )
        conn.commit()
        conn.close()

    def dump_database(self):
        conn = sql.connect(self.database_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM tab_count")
        rows = cur.fetchall()
        for row in rows:
            logger.info(row)
        conn.close()

    def drop_database(self):
        logger.info(f"Deleting database from {self.database_file}")
        os.remove(self.database_file)

    def print_dataframe(df: pd.DataFrame):
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(df)

    # Returns a dataframe with the columns: datetime, firefox_tab_count
    def get_database_values_as_dataframe(self) -> pd.DataFrame:
        conn = sql.connect(self.database_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM tab_count")
        rows = cur.fetchall()
        conn.close()
        df = pd.DataFrame(rows, columns=["datetime", "firefox_tab_count"])
        df['firefox_tab_count'].astype(int)
        return df
