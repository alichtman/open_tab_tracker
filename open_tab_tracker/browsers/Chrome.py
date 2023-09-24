from .Browser import Browser


class Chrome(Browser):
    """Abstract class for browser implementations."""

    def __init__(self):
        self.tab_count = self.get_tab_count()

    @classmethod
    def get_tab_count(self) -> int:
        """Returns an integer representing the max number of tabs open in the browser since the last time tab_status."""
        pass
