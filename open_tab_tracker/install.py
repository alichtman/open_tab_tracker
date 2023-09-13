import platform

#  import plistlib
import shutil
from loguru import logger
from enum import Enum
from subprocess import run, PIPE
from dataclasses import dataclass
from .filesystem import get_python_project_root_dir
from pathlib import Path
from os import getuid
import subprocess
import sys


@dataclass
class UnsupportedOSException(Exception):
    message: str = "Unsupported OS"

    def __str__(self):
        return f"Unsupported OS : {self.message}"


class SupportedOS(Enum):
    MACOS = "Darwin"
    LINUX = "Linux"


def get_current_os() -> SupportedOS:
    """Returns the current OS as a SupportedOS enum, and raises an UnsupportedOSException if the OS is not supported."""
    system = platform.system()
    if system == "Darwin":
        return SupportedOS.MACOS
    elif system == "Linux":
        return SupportedOS.LINUX
    else:
        raise UnsupportedOSException(f"Unsupported OS: {platform.system()}")


OS = get_current_os()


if OS == SupportedOS.MACOS:
    from launchd import plist
elif OS == SupportedOS.LINUX:
    # Install some systemd something
    pass


def install_systemd_service():
    pass


#########
# LAUNCHD
#########


LAUNCHD_SERVICE_NAME = "com.alichtman.open_tab_tracker"


def get_open_tab_tracker_executable_path():
    which = shutil.which("open_tab_tracker")
    if which:
        return which
    else:
        raise FileNotFoundError(
            "Could not find open_tab_tracker executable. Please install open_tab_tracker with `pip install open_tab_tracker`")


def install_launchd_service():
    plist_name = "com.alichtman.open_tab_tracker.plist"
    local_plist = (
        get_python_project_root_dir() / "open_tab_tracker/system_jobs" / plist_name
    )
    real_launch_agent_path = Path("/Library/LaunchAgents") / plist_name
    logger.info(f"Installing launchd service from {local_plist} to {real_launch_agent_path}")
    try:
        shutil.copy(local_plist, real_launch_agent_path)
        logger.info("Copied plist to /Library/LaunchAgents")
        with open(real_launch_agent_path, "r+") as f:
            marker = "{PATH_TO_OPEN_TAB_TRACKER_EXECUTABLE}"
            plist_contents = f.read().replace(marker, get_open_tab_tracker_executable_path())
            f.write(plist_contents)
    except PermissionError:
        logger.error(
            "Permission denied. Please run with sudo or as root to install launchd service."
        )
        sys.exit(1)

    ######
    # TODO: This does not work. Follow this guide: https://andypi.co.uk/2023/02/14/how-to-run-a-python-script-as-a-service-on-mac-os/

    # - Need to add variables to the launchd plist that I replace with system-specific paths
    ######
    logger.info("Loading launchd service")
    launchd_target = f"gui/{getuid()}/{LAUNCHD_SERVICE_NAME}"
    launchctl = "/bin/launchctl"
    run([launchctl, "bootstrap", launchd_target], stdout=PIPE, stderr=PIPE)
    run([launchctl, "kickstart", "-k", launchd_target], stdout=PIPE, stderr=PIPE)
    run(
        [
            launchctl,
            "load",
            real_launch_agent_path,
        ],
        stdout=PIPE,
        stderr=PIPE,
    )

    # Start launchd service


def uninstall_launchd_service():
    pass


def install_service_for_current_platform():
    if OS == SupportedOS.LINUX:
        logger.info("Installing systemd service")
        install_systemd_service()
        # TODO: Start job?
        pass
    elif OS == SupportedOS.MACOS:
        install_launchd_service()
        # TODO: Start job?
