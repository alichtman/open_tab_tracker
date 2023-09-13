from pathlib import Path
import subprocess
from shutil import which
from .browser import Browser
from ctypes import *
from .filesystem import get_python_project_root_dir

LZ4JSONCAT = "lz4jsoncat"
JQ = "jq"


class Firefox(Browser):
    # TODO: Finish integrating lz4jsoncat so
    @staticmethod
    def run_lz4jsoncat_on_file(file: Path) -> str:
        lz4jsoncat = CDLL(get_python_project_root_dir() / "lib/lz4jsoncat.so")
        print(lz4jsoncat)
        print("Running lz4jsoncat on file")
        print(file)
        print(lz4jsoncat.main(str(file)))
        return lz4jsoncat.main(str(file))

    @classmethod
    def check_for_deps(self):
        if which(LZ4JSONCAT) is None:
            raise Exception(
                "lz4jsoncat not found in $PATH. Please install it from https://github.com/andikleen/lz4json"
            )
        if which(JQ) is None:
            raise Exception(
                "jq not found in $PATH. Please install it from https://github.com/jqlang/jq"
            )

    @classmethod
    def get_firefox_recovery_file(self):
        """Returns the first recovery file found for Firefox, or None. Currently only works on macOS."""
        firefox_profiles = Path.home() / "Library/Application Support/Firefox/Profiles/"
        firefox_profiles = list(firefox_profiles.glob("*.default*"))
        if len(firefox_profiles) == 0:
            raise Exception(
                "No Firefox profiles found in ~/Library/Application Support/Firefox/Profiles/"
            )

        for profile in firefox_profiles:
            recovery_file = Path(profile) / "sessionstore-backups/recovery.jsonlz4"
            if recovery_file.exists():
                return recovery_file
        return None

    @classmethod
    def get_tab_count(self):
        recovery_file = Firefox.get_firefox_recovery_file()
        try:
            # unpacked_json = subprocess.run(
            #     [LZ4JSONCAT, recovery_file], stdout=subprocess.PIPE
            # ).stdout
            unpacked_json = Firefox.run_lz4jsoncat_on_file(recovery_file)
            tab_count = subprocess.run(
                [JQ, ".windows[].tabs | length"],
                input=unpacked_json,
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8")
            return tab_count
        except Exception as e:
            print(f"Something went wrong getting the tab count.\n\n{e}")
            return None
