from .database import Database
from .firefox import Firefox
from .graphing import draw_graph


def main():
    database = Database()
    firefox_tab_count = Firefox().tab_count
    print(f"Current firefox tab count: {firefox_tab_count}")
    database.write_to_database(firefox_tab_count)
    values = database.get_database_values()
    for time, value in values:
        print(f"{time}: {value}")

    from pprint import pprint
    pprint(values)
    draw_graph(values)

if __name__ == "__main__":
    main()
