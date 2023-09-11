import platform
from loguru import logger

if platform.system() == "darwin":
    from launchd import plist
elif platform.system() == "linux":
    # Install some systemd something
    pass


def install_systemd_service():
    pass


def install_launchd_service():
    sample_label = "com.alichtman.open_tab_tracker"
    sample_props = {
        {"Label": "testlaunchdwrapper_python"},
        {"StartInterval", 300},
        {
            "ProgramArguments": [
                "open-tab-tracker",
            ]
        },
    }

    plist.write(sample_label, sample_props, plist.USER)

def install():
    system = platform.system()

    symlink_binary()

    if system == "linux":
        logger.info("Installing systemd service")
        install_systemd_service()
        # TODO: Start job?
        pass
    elif system == "darwin":
        install_launchd_service()
        # TODO: Start job?
    else:
        raise Exception(f"Unsupported system: {system}")
