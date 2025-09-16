"""Silver contract for the Sandra Benes project."""

import pydantic

MIN_YEAR = 2012


class NormalizedHiveLogDocument(pydantic.BaseModel):
    """A normalized hive log ready for segmentation."""

    queen: str
    year: int = pydantic.Field(ge=MIN_YEAR)
    content: str
