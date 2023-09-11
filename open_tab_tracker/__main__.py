from .database import Database
from .firefox import Firefox
from .graphing import draw_graph
import click
from loguru import logger


@click.command()
@click.option("--daemon", is_flag=True, help="Run as a daemon")
@click.option("--graph", is_flag=True, help="Graph the data")
@click.option("--drop-database", is_flag=True, help="Drop the database")
def main(daemon, graph, drop_database):
    database = Database()
    if drop_database:
        logger.log("Dropping database")
        database.drop_database()
        return
    elif daemon:
        logger.log("Running as daemon")
        pass

    firefox_tab_count = Firefox().tab_count
    logger.info(f"Current firefox tab count: {firefox_tab_count}")
    database.write_to_database(firefox_tab_count)
    values = database.get_database_values_as_dataframe()

    from pprint import pprint
    pprint(values)
    if graph:
        draw_graph(values)
        pass


if __name__ == "__main__":
    main()
