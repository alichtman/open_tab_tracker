class Browser:
    """Abstract class for browser implementations."""

    def __init__(self):
        # self.check_for_deps()
        self.tab_count = self.get_tab_count()

    # @classmethod
    # def check_for_deps(self):
    #     """Checks for dependencies required to get the tab count from the browser.
    #     Raises an exception if a required dependency is not found."""
    #     pass

    @classmethod
    def get_tab_count(self) -> int:
        """Returns an integer representing the number of tabs open in the browser."""
        pass
