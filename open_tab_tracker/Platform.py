import platform
from enum import Enum
from loguru import logger


class OS(Enum):
    LINUX = 1
    MAC = 2
    WINDOWS = 3
    UNKNOWN = 4


class Platform:
    def __init__(self) -> None:
        self.current_os: OS = self.get_current_os()

    def get_current_os(self) -> OS:
        current_os = platform.system()
        match current_os:
            case "Linux":
                return OS.LINUX
            case "Darwin":
                return OS.MAC
            case "Windows":
                return OS.WINDOWS
            case _:
                return OS.UNKNOWN

    def validate(self):
        match self.current_os:
            case OS.LINUX:
                pass
            case OS.MAC:
                pass
            case OS.WINDOWS:
                raise NotImplementedError("Windows is not yet supported")
            case OS.UNKNOWN:
                raise NotImplementedError(f"This platform is not yet supported")
