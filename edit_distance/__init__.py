"""Python module for computing edit distances and alignments between sequences."""

from edit_distance.edit_distance import (
    DELETE,
    EQUAL,
    INSERT,
    REPLACE,
    edit_distance,
    edit_distance_backpointer,
)
from edit_distance.sequence_matcher import SequenceMatcher

__all__ = [
    "DELETE",
    "EQUAL",
    "INSERT",
    "REPLACE",
    "SequenceMatcher",
    "edit_distance",
    "edit_distance_backpointer",
]
