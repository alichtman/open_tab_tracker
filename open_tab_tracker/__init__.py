import click
from loguru import logger
import platform
from open_tab_tracker.__about__ import __version__
from .database import Database
from .graphing import draw_graph
from .install import install_crontab_entry, uninstall_crontab_entry


def validate_platform():
    match platform.system():
        case "Linux":
            pass
        case "Darwin":
            pass
        case "Windows":
            raise NotImplementedError("Windows is not yet supported")
        case _:
            raise NotImplementedError("Your platform is not yet supported")


@click.command(
    epilog="See the project homepage for more details: https://github.com/alichtman/open_tab_tracker",
    context_settings=dict(help_option_names=["-h", "-help", "--help"]),
)
@click.option("--add_datapoint", "-a", is_flag=True, help="Add a datapoint")
@click.option(
    "--install",
    "-i",
    is_flag=True,
    help="Install in crontab to run at startup",
)
@click.option(
    "--uninstall",
    is_flag=True,
    help="Uninstall from crontab",
)
@click.option("--drop-database", is_flag=True, help="Drop the database")
@click.option("--graph", is_flag=True, help="Opens the graph in a browser")
@click.option("--print_db", is_flag=True, help="Print the database")
@click.option("--version", "-v", is_flag=True, help="Print the version")
def run(add_datapoint, print_db, graph, install, drop_database, uninstall, version):
    """Open Tab Tracker"""
    validate_platform()
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
        database.add_current_tab_counts_to_db()
    else:
        draw_graph(database.get_database_values_as_dataframe())
