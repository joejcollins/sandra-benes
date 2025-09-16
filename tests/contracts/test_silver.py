"""Unit tests for the NormalizedHiveLogDocument model."""

import pydantic
import pytest

from sandra_benes.contracts import silver


def test_normalized_hive_log_document():
    """The earliest hive logs are from 2012, do there should be none earlier."""
    # ACT
    with pytest.raises(pydantic.ValidationError):
        silver.NormalizedHiveLogDocument(
            queen="Elizabeth", year=2011, content="#Invalid log\nEmpty."
        )
