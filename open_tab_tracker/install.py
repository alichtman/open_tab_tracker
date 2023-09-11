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


def install_launchd_service():
    local_plist = (
        get_python_project_root_dir()
        / "open_tab_tracker/system_jobs/com.alichtman.open_tab_tracker.plist"
    )
    launch_agents_dir = Path("/Library/LaunchAgents")
    logger.info(f"Installing launchd service from {local_plist} to {launch_agents_dir}")
    try:
        shutil.copy(local_plist, launch_agents_dir)
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
            "/Library/LaunchAgents/com.alichtman.open_tab_tracker.plist",
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
