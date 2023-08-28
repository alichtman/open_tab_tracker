from .database import Database
from .firefox import Firefox
from .graphing import draw_graph
import click


@click.command()
@click.option("--graph", is_flag=True, help="Graph the data")
@click.option("--drop-database", is_flag=True, help="Drop the database")
def main(graph, drop_database):
    database = Database()
    if drop_database:
        database.drop_database()
        return
    firefox_tab_count = Firefox().tab_count
    print(f"Current firefox tab count: {firefox_tab_count}")
    database.write_to_database(firefox_tab_count)
    values = database.get_database_values()
    for time, value in values:
        print(f"{time}: {value}")

    from pprint import pprint
    pprint(values)
    if graph:
        draw_graph(values)
        pass


if __name__ == "__main__":
    main()
