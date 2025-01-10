from datetime import datetime, timezone
from loguru import logger
import pandas as pd
from xdg_base_dirs import xdg_data_home
from .Platform import OS
from .browsers.Firefox import Firefox
import sqlite3 as sql
import os


class Database:
    def __init__(self):
        self.database_file = xdg_data_home() / "open_tab_tracker.db"
        self.create_db_and_datatable_if_not_exists()
        self.migrate_database_if_needed()

    def add_current_tab_counts_to_db(self, current_os: OS):
        logger.info("Adding datapoint!")
        firefox_tab_count = Firefox(current_os).tab_count
        if firefox_tab_count is not None:
            logger.info(f"Current firefox tab count: {firefox_tab_count}")
            self.write_to_database("firefox", firefox_tab_count)
        else:
            logger.error("Could not get Firefox tab count. Skipping.")

    @staticmethod
    def convert_utc_datetime_to_local_formatted_string(utc_time_str: str):
        utc_datetime: datetime = datetime.strptime(
            utc_time_str, "%Y-%m-%d %H:%M:%S.%f%z"
        )
        current_timezone = utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)
        # logger.debug(f"Converted {utc_time_str} to {current_timezone}")
        return current_timezone.strftime("%m/%d/%y %I:%M%p")

    def create_db_and_datatable_if_not_exists(self):
        conn = sql.connect(self.database_file)
        logger.info(
            f"Creating database (if didn't already exist) at {self.database_file}"
        )
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS browser_tab_count (datetime TEXT, browser_type TEXT, tab_count INTEGER)"
        )
        conn.commit()

    def write_to_database(self, browser_type: str, tab_count: int):
        """Write the tab counts to the database, along with the current time in UTC"""
        utc_current_time = datetime.now(tz=timezone.utc)
        conn = sql.connect(self.database_file)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO browser_tab_count ('datetime', 'browser_type', 'tab_count') VALUES (?, ?, ?)",
            (utc_current_time, browser_type, tab_count),
        )
        conn.commit()
        conn.close()

    def dump_database(self):
        conn = sql.connect(self.database_file)
        cur = conn.cursor()
        
        # Dump old table if it exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tab_count'")
        if cur.fetchone() is not None:
            logger.info("Dumping old tab_count table:")
            cur.execute("SELECT * FROM tab_count")
            rows = cur.fetchall()
            for row in rows:
                logger.info(row)
        
        # Dump new table
        logger.info("Dumping browser_tab_count table:")
        cur.execute("SELECT * FROM browser_tab_count") 
        rows = cur.fetchall()
        for row in rows:
            logger.info(row)
            
        conn.close()

    def drop_database(self):
        logger.warning(f"Deleting database from {self.database_file}")
        os.remove(self.database_file)

    def print_database(self):
        self.print_dataframe(self.get_database_values_as_dataframe())

    def print_dataframe(self, df: pd.DataFrame):
        with pd.option_context("display.max_rows", None, "display.max_columns", None):
            print(df)

    # Returns a dataframe with the columns: datetime, firefox_tab_count
    def get_database_values_as_dataframe(self) -> pd.DataFrame:
        conn = sql.connect(self.database_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM browser_tab_count")
        rows = cur.fetchall()
        conn.close()
        df = pd.DataFrame(rows, columns=["datetime", "browser_type", "tab_count"])
        df["datetime"] = df["datetime"].apply(
            lambda x: self.convert_utc_datetime_to_local_formatted_string(x)
        )
        df["tab_count"] = df["tab_count"].astype(int)
        return df

    def migrate_database_if_needed(self):
        """Migrate data from old table (tab_count) to new table (browser_tab_count)"""
        conn = sql.connect(self.database_file)
        cursor = conn.cursor()
        
        # Check if old table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tab_count'")
        old_table_exists = cursor.fetchone() is not None
        
        if old_table_exists:
            logger.info("Found old table 'tab_count', migrating data...")
            
            # Check if data was already migrated by looking for any records in new table
            cursor.execute("SELECT COUNT(*) FROM browser_tab_count")
            new_table_count = cursor.fetchone()[0]
            
            if new_table_count == 0:
                # Copy data from old table to new table
                cursor.execute("""
                    INSERT INTO browser_tab_count (datetime, browser_type, tab_count)
                    SELECT datetime, 'firefox', firefox_tab_count
                    FROM tab_count
                """)
                
                conn.commit()
                logger.info("Data migration completed successfully")
                logger.info("Old 'tab_count' table preserved for backup")
            else:
                logger.info("New table already contains data, skipping migration")
        
        conn.close()
