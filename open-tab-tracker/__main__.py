from .database import Database
from .firefox import Firefox


def main():
    database = Database()
    print(f"Database: {database}")
    firefox_tab_count = Firefox().tab_count
    print(f"Current firefox tab count: {firefox_tab_count}")
    database.write_to_database(firefox_tab_count)
    database.dump_database()
    values = database.get_database_values()
    for time, value in values:
        print(f"{time}: {value}")


if __name__ == "__main__":
    main()
