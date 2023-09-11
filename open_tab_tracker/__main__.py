from .database import Database
from .firefox import Firefox
from .graphing import draw_graph
from .install import install_service_for_current_platform
import click
from loguru import logger
import sys


def get_current_tab_count_and_write_to_database(database: Database):
    firefox_tab_count = Firefox().tab_count
    logger.info(f"Current firefox tab count: {firefox_tab_count}")
    database.write_to_database(firefox_tab_count)


@click.command()
@click.option("--add_datapoint", "-a", is_flag=True, help="Add a datapoint")
@click.option("--daemon", is_flag=True, help="Run as a daemon")
@click.option(
    "--install",
    is_flag=True,
    help="Automatically install the daemon and run at startup",
)
@click.option("--graph", is_flag=True, help="Graph the data")
@click.option("--drop-database", is_flag=True, help="Drop the database")
@click.option("--print_db", is_flag=True, help="Print the database")
def main(add_datapoint, daemon, graph, print_db, install, drop_database):
    database = Database()
    if drop_database:
        logger.warning("Dropping database")
        database.drop_database()
        return
    elif print_db:
        database.print_database()
        sys.exit(0)
    elif install:
        logger.info("Installing daemon")
        install_service_for_current_platform()
        sys.exit(0)

    if add_datapoint:
        get_current_tab_count_and_write_to_database(database)

    if graph:
        draw_graph(database.get_database_values_as_dataframe())
        pass


if __name__ == "__main__":
    main()
