from rich.console import Console
import shutil
from loguru import logger
from pathlib import Path
import inspect, os.path
from crontab import CronTab, CronItem

console = Console()


def get_open_tab_tracker_executable_path():
    # Check if executable is installed on $PATH
    which = shutil.which("open_tab_tracker")
    if which:
        logger.info("Found open_tab_tracker executable at {which}")
        return which
    else:
        # Maybe we're in the hatch dev env? We can grab the bin path from the filename
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        logger.info(f"Filename: {filename}")
        path = os.path.dirname(os.path.abspath(filename))
        pkg_name = "open-tab-tracker"
        path = filename[: filename.rfind(f"{pkg_name}/")] + f"{pkg_name}/bin/{pkg_name}"
        logger.info(f"Path: {path}")
        if Path(path).exists():
            logger.info(f"Found open_tab_tracker executable in hatch dev env at {path}")
            return path
        else:
            raise FileNotFoundError(
                "Could not find open_tab_tracker executable. Make sure it is on your $PATH. You can check with `$ which open_tab_tracker`"
            )


CRONTAB_COMMENT = "open_tab_tracker"


def get_crontab_entries(cron: CronTab) -> list[CronItem] | None:
    entries = list(cron.find_comment(CRONTAB_COMMENT))
    if len(entries) == 0:
        return None
    else:
        return entries


def install_crontab_entry():
    user_cron = CronTab(user=True)
    existing_entries = get_crontab_entries(user_cron)
    if existing_entries:
        logger.info("Crontab entries already exist. Skipping.")
        return

    job = user_cron.new(
        command=f'PATH=$PATH:{shutil.which("lz4jsoncat")} "{get_open_tab_tracker_executable_path()}" --add_datapoint',
        comment=CRONTAB_COMMENT,
    )
    job.minute.every(1)
    job.run()
    user_cron.write()
    logger.info("Added a new crontab entry.")


def uninstall_crontab_entry():
    logger.info("Removing crontab entry if it exists...")
    user_cron = CronTab(user=True)
    user_cron.remove_all(comment=CRONTAB_COMMENT)
    user_cron.write()
