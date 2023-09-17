from pathlib import Path
from typing import Any, Dict
from .browser import Browser
import lz4.block
import jq
import json


class Firefox(Browser):
    @staticmethod
    def lz4json_decompress_file(file: Path) -> Dict[str, Any]:
        """Decompresses a Firefox recovery file and returns a JSON dictionary.
        Mozilla uses a non-standard format for their LZ4 compressed recovery files: https://superuser.com/a/1363751
        The first 8 bytes of the file are `mozLz40`, the next 4 bytes (little endian int) are the uncompressed size,
        and all data afterwards is the compressed data.

        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |     mozLz40   | size  |   compressed data.... |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        """
        with open(file, "rb") as f:
            magic = f.read(8)
            if magic != b"mozLz40\0":
                raise Exception("Not a Firefox recovery file")
            f.seek(8)
            uncompressed_size = int.from_bytes(f.read(4), byteorder="little")
            f.seek(12)
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
            unpacked_json: Dict[str, Any] = Firefox.lz4json_decompress_file(
                recovery_file
            )
            tab_count = (
                jq.compile(".windows[].tabs | length").input(unpacked_json).first()
            )
            return tab_count
        except Exception as e:
            print(f"Something went wrong getting the tab count.\n\n{e}")
            return None
