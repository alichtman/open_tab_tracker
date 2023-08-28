from datetime import datetime, timezone
from loguru import logger
from typing import List, Tuple
from xdg_base_dirs import xdg_data_home
import sqlite3 as sql
import os


class Database:
    def __init__(self):
        self.database_file = xdg_data_home() / "open-tab-tracker.db"
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
        tz_aware_datetime = datetime.now(timezone.utc)
        conn = sql.connect(self.database_file)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tab_count ('datetime', 'firefox_tab_count') VALUES (?, ?)",
            (tz_aware_datetime, firefox_tab_count),
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

    def get_database_values(self) -> List[Tuple[datetime, int]]:
        conn = sql.connect(self.database_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM tab_count")
        rows = cur.fetchall()
        conn.close()
        return rows
