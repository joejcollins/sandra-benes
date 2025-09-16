"""Confirm that the file iterator works as expected."""

from pathlib import Path

from sandra_benes.helpers import file_iterator


def test_reads_files_in_sorted_order(tmp_path: Path):
    """It should read files in sorted order by filename."""
    # ARRANGE
    (tmp_path / "b.txt").write_text("bee")
    (tmp_path / "a.txt").write_text("aye")
    (tmp_path / "c.log").write_text("log")
    # ACT
    contents = list(file_iterator.file_contents(tmp_path, "*.txt"))
    # ASSERT
    assert contents == ["aye", "bee"]
