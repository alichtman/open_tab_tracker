from pathlib import Path
from typing import Any, Dict, Optional
from loguru import logger
import os
from open_tab_tracker.Platform import Platform, OS
from .Browser import Browser
import lz4.block
import jq
import json


class Firefox(Browser):
    def __init__(self, current_os: OS):
        super().__init__(current_os)

    @staticmethod
    def lz4json_decompress_file(file: Path) -> Dict[str, Any]:
        """Decompresses a Firefox recovery file and returns a JSON dictionary.
        Mozilla uses a non-standard format for their LZ4 compressed recovery files: https://superuser.com/a/1363751
        The first 8 bytes of the file are `mozLz40`, the next 4 bytes (little endian int) are the uncompressed size,
        and all data afterwards is the compressed data.

        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |m o z L z 4 0  | size  | LZ4 compressed data   |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        """
        with open(file, "rb") as f:
            magic = f.read(8)
            if magic != b"mozLz40\0":
                raise Exception("Not a Firefox recovery file")
            uncompressed_size = int.from_bytes(f.read(4), byteorder="little")
            compressed = f.read()
            try:
                decompressed = lz4.block.decompress(compressed, uncompressed_size)
            except lz4.block.LZ4BlockError:
                raise Exception("Something wrong with lz4 decompression")
        try:
            decompressed = json.loads(decompressed)
            return decompressed
        except json.decoder.JSONDecodeError:
            raise Exception("Something wrong with JSON decoding")

    @classmethod
    def get_firefox_recovery_file(self):
        """Returns the latest recovery file found for Firefox, or None."""
        firefox_profile_paths: list[Path] = []
        match Platform().get_current_os():
            case OS.MAC:
                firefox_profile_paths.append(
                    Path.home() / "Library/Application Support/Firefox/Profiles/"
                )
            case OS.LINUX:
                firefox_profile_paths.extend([
                    Path.home() / "snap/firefox/common/.mozilla/firefox/",
                    Path.home() / ".mozilla/firefox/"
                ])
            case OS.WINDOWS:
                firefox_profile_paths.extend([
                    Path(os.environ["APPDATA"]) / "Mozilla/Firefox/Profiles/",
                    Path(os.environ["LOCALAPPDATA"]) / "Packages/Mozilla.Firefox/LocalCache/Roaming/Mozilla/Firefox/Profiles/"
                ])

        firefox_profiles = [
            profile
            for profile_path_candidate in firefox_profile_paths
            for profile in profile_path_candidate.glob("*.default*")
        ]
        if len(firefox_profiles) == 0:
            raise Exception(f"No Firefox profiles found in {firefox_profile_paths}")

        latest_recovery: Optional[Path] = None
        latest_time = 0
        for profile in firefox_profiles:
            logger.info(f"Checking for recovery file in {profile}")
            recovery_file = Path(profile) / "sessionstore-backups/recovery.jsonlz4"
            if recovery_file.exists():
                mod_time = recovery_file.stat().st_mtime
                if mod_time > latest_time:
                    latest_time = mod_time
                    latest_recovery = recovery_file
        return latest_recovery

    @classmethod
    def get_tab_count(self):
        """
        Inside the recovery file JSON, tabs are stored in this structure:

        windows: [                 # Array of all windows
            "tabs": [              # Each window has an array of tabs
                {
                    "entries": [   # And each tab stores its history in an array of entries
                        {
                            "url": "https://www.google.com/",
                            "title": "Google",
                            ...
                        },
                        ...
                    ],
                },
                ...
            ],
            ...
        ]

        We can use jq to sum the lengths of all the tabs arrays:
        [.windows[].tabs | length] | add
        """
        recovery_file = Firefox.get_firefox_recovery_file()
        try:
            unpacked_json: Dict[str, Any] = Firefox.lz4json_decompress_file(
                recovery_file
            )
            tab_count = (
                jq.compile("[.windows[].tabs | length] | add")
                .input(unpacked_json)
                .first()
            )
            return tab_count
        except Exception as e:
            print(f"Something went wrong getting the tab count.\n\n{e}")
            return None
