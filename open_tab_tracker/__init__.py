import click
import logging.handlers
from logging.handlers import SysLogHandler
from loguru import logger
from open_tab_tracker.__about__ import __version__
from .Database import Database
from .graphing import draw_graph
from .install import install_crontab_entry, uninstall_crontab_entry
from .Platform import Platform


def configure_logging_to_syslog():
    handler = logging.handlers.SysLogHandler(
        facility=SysLogHandler.LOG_DAEMON, address="/dev/log"
    )
    logger.add(handler)


@click.command(
    epilog="See the project homepage for more details: https://github.com/alichtman/open_tab_tracker",
    context_settings=dict(help_option_names=["-h", "-help", "--help"]),
)
@click.option("--add-datapoint", "-a", is_flag=True, help="Add a datapoint")
@click.option(
    "--install",
    "-i",
    is_flag=True,
    help="Install in crontab to run at startup",
)
@click.option("--drop-database", is_flag=True, help="Drop the database")
@click.option("--graph", is_flag=True, help="Opens the graph in a browser")
@click.option("--print-db", is_flag=True, help="Print the database")
@click.option(
    "--uninstall",
    is_flag=True,
    help="Uninstall from crontab",
)
@click.option("--version", "-v", is_flag=True, help="Print the version")
def run(add_datapoint, print_db, graph, install, drop_database, uninstall, version):
    """Open Tab Tracker"""
    configure_logging_to_syslog()
    platform = Platform()
    platform.validate()
    if version:
        print(f"open-tab-tracker {__version__}")
        return
    database = Database()
    if drop_database:
        database.drop_database()
        return
    elif print_db:
        database.print_database()
        return
    elif install:
        install_crontab_entry()
        return
    elif uninstall:
        uninstall_crontab_entry()
        return
    elif graph:
        draw_graph(database.get_database_values_as_dataframe())
        return
    elif add_datapoint:
        database.add_current_tab_counts_to_db(platform.current_os)
    else:
        draw_graph(database.get_database_values_as_dataframe())
