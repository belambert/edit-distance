# -*- mode: Python;-*-

# Copyright 2013-2020 Ben Lambert

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A difflib-style interface to the edit distance routines.
"""

import operator
from collections.abc import Sequence

from edit_distance.edit_distance import (
    EQUAL,
    GapCostFunction,
    SubstitutionCostFunction,
    TestFunction,
    edit_distance,
    edit_distance_backpointer,
)


# Two sequences, four comparison/cost hooks, and three cached results.
# pylint: disable-next=too-many-instance-attributes
class SequenceMatcher:
    """
    Similar to the :py:mod:`difflib` :py:class:`~difflib.SequenceMatcher`, but
    uses Levenshtein/edit distance.
    """

    def __init__(
        self,
        a: Sequence | None = None,
        b: Sequence | None = None,
        test: TestFunction = operator.eq,
        *,
        substitution_cost: SubstitutionCostFunction | None = None,
        insertion_cost: GapCostFunction | None = None,
        deletion_cost: GapCostFunction | None = None,
    ):
        """
        Initialize the object with sequences a and b.  Optionally, one can
        specify a test function that is used to compare sequence elements. This
        defaults to the built in ``eq`` operator (i.e. :py:func:`operator.eq`).

        The three cost functions are passed straight through to
        :py:func:`~edit_distance.edit_distance`; see that function for what
        they mean and what they default to.
        """
        if a is None:
            a = []
        if b is None:
            b = []
        self.seq1 = a
        self.seq2 = b
        self._reset_object()
        self.test = test
        self.substitution_cost = substitution_cost
        self.insertion_cost = insertion_cost
        self.deletion_cost = deletion_cost
        self.dist: float | None = None
        self._matches: int | None = None
        self.opcodes = None

    def set_seqs(self, a: Sequence, b: Sequence) -> None:
        """Specify two alternative sequences -- reset any cached values."""
        self.set_seq1(a)
        self.set_seq2(b)
        self._reset_object()

    def _reset_object(self) -> None:
        """Clear out the cached values for distance, matches, and opcodes."""
        self.opcodes = None
        self.dist = None
        self._matches = None

    def set_seq1(self, a: Sequence) -> None:
        """Specify a new sequence for sequence 1, resetting cached values."""
        self._reset_object()
        self.seq1 = a

    def set_seq2(self, b: Sequence) -> None:
        """Specify a new sequence for sequence 2, resetting cached values."""
        self._reset_object()
        self.seq2 = b

    def find_longest_match(self, alo, ahi, blo, bhi) -> None:
        """Not implemented!"""
        raise NotImplementedError()

    def get_matching_blocks(self):
        """Similar to :py:meth:`get_opcodes`, but returns only the opcodes that are
        equal and returns them in a somewhat different format
        (i.e. ``(i, j, n)`` )."""
        opcodes = self.get_opcodes()
        match_opcodes = filter(lambda x: x[0] == EQUAL, opcodes)
        return map(
            lambda opcode: [opcode[1], opcode[3], opcode[2] - opcode[1]], match_opcodes
        )

    def get_opcodes(self):
        """Returns a list of opcodes.  Opcodes are the same as defined by
        :py:mod:`difflib`."""
        if self.opcodes is None:
            d, m, opcodes = edit_distance_backpointer(
                self.seq1,
                self.seq2,
                test=self.test,
                substitution_cost=self.substitution_cost,
                insertion_cost=self.insertion_cost,
                deletion_cost=self.deletion_cost,
            )
            if self.dist is not None:
                assert d == self.dist
            if self._matches is not None:
                assert m == self._matches
            self.dist = d
            self._matches = m
            self.opcodes = opcodes
        return self.opcodes

    def get_grouped_opcodes(self, n=None):
        """Not implemented!"""
        raise NotImplementedError()

    def ratio(self) -> float:
        """Ratio of matches to the average sequence length."""
        if not self.seq1 and not self.seq2:
            return 1.0
        return 2.0 * self.matches() / (len(self.seq1) + len(self.seq2))

    def quick_ratio(self) -> float:
        """Same as :py:meth:`ratio`."""
        return self.ratio()

    def real_quick_ratio(self) -> float:
        """Same as :py:meth:`ratio`."""
        return self.ratio()

    def _compute_distance_fast(self) -> None:
        """Calls edit_distance, and asserts that if we already have values for
        matches and distance, that they match."""
        d, m = edit_distance(
            self.seq1,
            self.seq2,
            test=self.test,
            substitution_cost=self.substitution_cost,
            insertion_cost=self.insertion_cost,
            deletion_cost=self.deletion_cost,
        )
        if self.dist is not None:
            assert d == self.dist
        if self._matches is not None:
            assert m == self._matches
        self.dist = d
        self._matches = m

    def distance(self):
        """Returns the edit distance of the two loaded sequences.  This should
        be a little faster than getting the same information from
        :py:meth:`get_opcodes`."""
        if self.dist is None:
            self._compute_distance_fast()
        return self.dist

    def matches(self):
        """Returns the number of matches in the alignment of the two sequences.
        This should be a little faster than getting the same information from
        :py:meth:`get_opcodes`."""
        if self._matches is None:
            self._compute_distance_fast()
        return self._matches
