from shutil import which
from pathlib import Path
import subprocess

LZ4JSONCAT = "lz4jsoncat"
JQ = "jq"


def get_firefox_recovery_files():
    """ Returns a list of recovery files for Firefox. Currently only works on macOS."""
    firefox_profiles = Path.home() / "Library/Application Support/Firefox/Profiles/"
    firefox_profiles = list(firefox_profiles.glob("*.default*"))
    if len(firefox_profiles) == 0:
        raise Exception("No Firefox profiles found in ~/Library/Application Support/Firefox/Profiles/")

    recovery_files: [Path] = []
    for profile in firefox_profiles:
        recovery_file = Path(profile) / "sessionstore-backups/recovery.jsonlz4"
        if recovery_file.exists():
            recovery_files.append(recovery_file)
    return recovery_files


def get_firefox_tab_count_sum(recovery_file: Path):
    try:
        unpacked_json = subprocess.run([LZ4JSONCAT, recovery_file], stdout=subprocess.PIPE).stdout
        tab_count = subprocess.run(["jq", ".windows[].tabs | length"], input=unpacked_json, stdout=subprocess.PIPE).stdout.decode("utf-8")
        return tab_count
    except Exception as e:
        print(f"Something went wrong getting the tab count.\n\n{e}")
        return None


def check_for_deps():
    if which(LZ4JSONCAT) is None:
        raise Exception("lz4jsoncat not found in $PATH. Please install it from https://github.com/andikleen/lz4json")
    if which(JQ) is None:
        raise Exception("jq not found in $PATH. Please install it from https://github.com/jqlang/jq")


def main():
    check_for_deps()
    recovery_files = get_firefox_recovery_files()
    for recovery_file in recovery_files:
        firefox_tab_count = get_firefox_tab_count_sum(recovery_file)
        print(f"Current firefox tab count: {firefox_tab_count}")


if __name__ == "__main__":
    main()
