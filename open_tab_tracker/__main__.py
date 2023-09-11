from .database import Database
from .firefox import Firefox
from .graphing import draw_graph
import click
from loguru import logger


def get_current_tab_count_and_write_to_database(database: Database):
    firefox_tab_count = Firefox().tab_count
    logger.info(f"Current firefox tab count: {firefox_tab_count}")
    database.write_to_database(firefox_tab_count)


@click.command()
@click.option("--daemon", is_flag=True, help="Run as a daemon")
@click.option(
    "--install",
    is_flag=True,
    help="Automatically install the daemon and run at startup",
)
@click.option("--graph", is_flag=True, help="Graph the data")
@click.option("--drop-database", is_flag=True, help="Drop the database")
def main(daemon, graph, install, drop_database):
    database = Database()
    if drop_database:
        logger.log("Dropping database")
        database.drop_database()
        return
    elif daemon:
        logger.log("Running as daemon")
        register_daemon()
        # Start background job to log tab counts every 5 minutes
        pass
    elif install:
        logger.log("Installing daemon")
        pass

    get_current_tab_count_and_write_to_database(database)

    if graph:
        draw_graph(database.get_database_values_as_dataframe())
        pass


if __name__ == "__main__":
    main()
