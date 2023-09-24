from open_tab_tracker.Platform import OS


class Browser:
    """Abstract class for browser implementations."""

    def __init__(self, current_os: OS):
        self.tab_count = self.get_tab_count()
        self.current_os: OS = current_os


    @classmethod
    def get_tab_count(self) -> int:
        """Returns an integer representing the number of tabs open in the browser."""
        pass
