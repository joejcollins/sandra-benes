"""Data reader for raw hive logs in the Sandra Benes project."""


class HiveLogsReader:
    """Iterate through the hive logs."""

    def __init__(self, directory_path: str) -> None:
        """Initialize the reader with the path to the raw hive log files."""
        self.directory_path = directory_path
