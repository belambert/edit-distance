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
Unit tests for edit_distance.
"""

import unittest

from edit_distance import SequenceMatcher, edit_distance, edit_distance_backpointer


class TestEditDistance(unittest.TestCase):
    """Class to hold all the tests for this package."""

    def test_edit_distance0(self):
        """Test edit distance between 'ab' and 'dab'."""
        a = ["a", "b"]
        b = ["d", "a", "b"]
        self.assertEqual(edit_distance(a, b), (1, 2))
        bp_expected_result = (
            1,
            2,
            [["insert", 0, 0, 0, 1], ["equal", 0, 1, 1, 2], ["equal", 1, 2, 2, 3]],
        )
        self.assertEqual(edit_distance_backpointer(a, b), bp_expected_result)

    def test_edit_distance1(self):
        """Test edit distance between 'ab' and 'acdab'."""
        a = ["a", "b"]
        b = ["a", "c", "d", "a", "b"]
        self.assertEqual(edit_distance(a, b), (3, 2))
        bp_expected_result = (
            3,
            2,
            [
                ["insert", 0, 0, 0, 1],
                ["insert", 0, 0, 1, 2],
                ["insert", 0, 0, 2, 3],
                ["equal", 0, 1, 3, 4],
                ["equal", 1, 2, 4, 5],
            ],
        )
        self.assertEqual(edit_distance_backpointer(a, b), bp_expected_result)

    def test_edit_distance2(self):
        """Test edit distance for 'hi my name is andy'."""
        a = ["hi", "my", "name", "is", "andy"]
        b = ["hi", "i'm", "my", "name's", "sandy"]
        self.assertEqual(edit_distance(a, b), (4, 1))
        bp_expected_result = (
            4,
            1,
            [
                ["equal", 0, 1, 0, 1],
                ["replace", 1, 2, 1, 2],
                ["replace", 2, 3, 2, 3],
                ["replace", 3, 4, 3, 4],
                ["replace", 4, 5, 4, 5],
            ],
        )
        self.assertEqual(edit_distance_backpointer(a, b), bp_expected_result)

    def test_substitution_cost_reproduces_highest_match_alignment(self):
        """Pricing a mismatched substitution at exactly insertion + deletion
        recovers the alignment the removed highest_match_action produced: the
        same opcodes and the same two matches.  The distance is 6 rather than
        that function's 4 because it is now measured in the new cost units --
        highest_match_action accumulated unit costs while choosing by match
        count, which a cost function cannot do."""
        a = ["hi", "my", "name", "is", "andy"]
        b = ["hi", "i'm", "my", "name's", "sandy"]
        sub = lambda x, y: 0 if x == y else 2  # noqa: E731
        self.assertEqual(edit_distance(a, b, substitution_cost=sub), (6, 2))
        bp_expected_result = (
            6,
            2,
            [
                ["equal", 0, 1, 0, 1],
                ["insert", 1, 1, 1, 2],
                ["equal", 1, 2, 2, 3],
                ["delete", 2, 3, 3, 3],
                ["replace", 3, 4, 3, 4],
                ["replace", 4, 5, 4, 5],
            ],
        )
        self.assertEqual(
            edit_distance_backpointer(a, b, substitution_cost=sub),
            bp_expected_result,
        )

    def test_substitution_costing_more_than_a_gap_pair_is_never_chosen(self):
        """A substitution dearer than insertion + deletion is routed around,
        so no replace survives even though the match count is unchanged."""
        a = ["hi", "my", "name", "is", "andy"]
        b = ["hi", "i'm", "my", "name's", "sandy"]
        sub = lambda x, y: 0 if x == y else 3  # noqa: E731
        dist, matches, opcodes = edit_distance_backpointer(a, b, substitution_cost=sub)
        self.assertEqual((dist, matches), (6, 2))
        self.assertNotIn("replace", [op[0] for op in opcodes])

    def test_match_can_cost_something(self):
        """A custom substitution cost is consulted for equal pairs too, so
        identical sequences need not be free.  The pair is still an ``equal``
        and still counts as a match, since ``test`` decides that, not cost."""
        dist, matches, opcodes = edit_distance_backpointer(
            ["a"], ["a"], substitution_cost=lambda x, y: 0.5
        )
        self.assertAlmostEqual(dist, 0.5)
        self.assertEqual(matches, 1)
        self.assertEqual(opcodes, [["equal", 0, 1, 0, 1]])

    def test_zero_cost_substitution_is_not_a_match(self):
        """The converse: a free substitution that ``test`` rejects is still a
        replace and still does not count as a match."""
        never_eq = lambda x, y: False  # noqa: E731
        dist, matches, opcodes = edit_distance_backpointer(
            ["a", "b"], ["a", "b"], test=never_eq, substitution_cost=lambda x, y: 0
        )
        self.assertEqual((dist, matches), (0, 0))
        self.assertEqual(opcodes, [["replace", 0, 1, 0, 1], ["replace", 1, 2, 1, 2]])

    def test_insertion_cost_accumulates_over_an_empty_seq1(self):
        """With nothing to align against, the distance is the sum of the
        per-element insertion costs rather than the number of insertions."""
        b = ["a", "bb", "ccc"]
        self.assertEqual(edit_distance([], b, insertion_cost=len), (6, 0))
        self.assertEqual(
            edit_distance_backpointer([], b, insertion_cost=len),
            (
                6,
                0,
                [
                    ["insert", 0, 0, 0, 1],
                    ["insert", 0, 0, 1, 2],
                    ["insert", 0, 0, 2, 3],
                ],
            ),
        )

    def test_deletion_cost_accumulates_over_an_empty_seq2(self):
        """The same, for the deletion boundary."""
        a = ["a", "bb", "ccc"]
        self.assertEqual(edit_distance(a, [], deletion_cost=len), (6, 0))
        self.assertEqual(
            edit_distance_backpointer(a, [], deletion_cost=len),
            (
                6,
                0,
                [
                    ["delete", 0, 1, 0, 0],
                    ["delete", 1, 2, 0, 0],
                    ["delete", 2, 3, 0, 0],
                ],
            ),
        )

    def test_cheap_gaps_beat_a_substitution(self):
        """Custom gap costs move the cap on substitution: when a deletion plus
        an insertion is cheaper than replacing, the search prefers them."""
        cheap = lambda elem: 0.1  # noqa: E731
        dist, matches, opcodes = edit_distance_backpointer(
            ["x"], ["y"], insertion_cost=cheap, deletion_cost=cheap
        )
        self.assertAlmostEqual(dist, 0.2)
        self.assertEqual(matches, 0)
        self.assertEqual(opcodes, [["delete", 0, 1, 0, 0], ["insert", 1, 1, 0, 1]])

    def test_per_element_insertion_cost(self):
        """Insertion cost can depend on the element, so a filler word can be
        cheaper to insert than a content word."""
        ref = ["i", "want", "coffee"]
        hyp = ["i", "um", "want", "coffee"]
        filler_is_cheap = lambda y: 0.1 if y == "um" else 1  # noqa: E731
        dist, matches = edit_distance(ref, hyp, insertion_cost=filler_is_cheap)
        self.assertAlmostEqual(dist, 0.1)
        self.assertEqual(matches, 3)
        self.assertEqual(edit_distance(ref, hyp), (1, 3))

    def test_sequence_matcher_uses_cost_functions(self):
        """SequenceMatcher passes the cost functions to both the fast path and
        the backpointer path, which must agree on distance and matches."""
        cheap = lambda elem: 0.1  # noqa: E731
        kwargs = {"insertion_cost": cheap, "deletion_cost": cheap}
        expected_opcodes = [["delete", 0, 1, 0, 0], ["insert", 1, 1, 0, 1]]

        # Distance first, so the fast path populates the cache.
        sm = SequenceMatcher(a=["x"], b=["y"], **kwargs)
        self.assertAlmostEqual(sm.distance(), 0.2)
        self.assertEqual(sm.get_opcodes(), expected_opcodes)

        # Opcodes first, so the backpointer path populates it instead.
        sm = SequenceMatcher(a=["x"], b=["y"], **kwargs)
        self.assertEqual(sm.get_opcodes(), expected_opcodes)
        self.assertAlmostEqual(sm.distance(), 0.2)
        self.assertEqual(sm.matches(), 0)

        # Matches first, which reaches the fast path through a third door.
        sm = SequenceMatcher(a=["x"], b=["y"], **kwargs)
        self.assertEqual(sm.matches(), 0)
        self.assertAlmostEqual(sm.distance(), 0.2)
        self.assertEqual(sm.get_opcodes(), expected_opcodes)

    def test_cost_functions_are_keyword_only(self):
        """Everything after the two sequences is keyword-only, so a stray
        positional argument fails loudly instead of being read as ``test``."""
        with self.assertRaises(TypeError):
            edit_distance(["a"], ["b"], lambda x, y: True)
        with self.assertRaises(TypeError):
            edit_distance_backpointer(["a"], ["b"], lambda x, y: True)

    def test_edit_distance3(self):
        """Test for 'are you at work now'."""
        a = ["are", "you", "at", "work", "now"]
        b = ["i", "feel", "are", "saying"]
        bp_expected_result = (
            5,
            0,
            [
                ["delete", 0, 1, 0, 0],
                ["replace", 1, 2, 0, 1],
                ["replace", 2, 3, 1, 2],
                ["replace", 3, 4, 2, 3],
                ["replace", 4, 5, 3, 4],
            ],
        )
        self.assertEqual(edit_distance_backpointer(a, b), bp_expected_result)

    def test_edit_distance4(self):
        """Test edit distance against an empty list."""
        a = []
        b = ["a", "c"]
        self.assertEqual(edit_distance(a, b), (2, 0))
        self.assertEqual(edit_distance(b, a), (2, 0))
        self.assertEqual(edit_distance(a, a), (0, 0))

    def test_edit_distance_backpointer_empty(self):
        """Test the backpointer version against empty sequences."""
        a = []
        b = ["a", "c"]
        b_opcodes = [["insert", 0, 0, 0, 1], ["insert", 0, 0, 1, 2]]
        a_opcodes = [["delete", 0, 1, 0, 0], ["delete", 1, 2, 0, 0]]
        self.assertEqual(edit_distance_backpointer(a, b), (2, 0, b_opcodes))
        self.assertEqual(edit_distance_backpointer(b, a), (2, 0, a_opcodes))
        self.assertEqual(edit_distance_backpointer(a, a), (0, 0, []))

    def test_distance_then_opcodes(self):
        """Distance computed via the fast path must agree with the
        backpointer path (regression test for empty seq1)."""
        sm = SequenceMatcher(a=[], b=["a"])
        self.assertEqual(sm.distance(), 1)
        self.assertEqual(sm.get_opcodes(), [["insert", 0, 0, 0, 1]])

    def test_ratio_empty(self):
        """Two empty sequences are identical, so ratio is 1.0."""
        self.assertEqual(SequenceMatcher(a=[], b=[]).ratio(), 1.0)
        self.assertEqual(SequenceMatcher(a=[], b=[]).distance(), 0)

    def test_custom_test_function(self):
        """A custom test function must be honored even when the sequences
        compare equal with ==."""
        a = ["a", "b"]
        never_eq = lambda x, y: False  # noqa: E731
        self.assertEqual(edit_distance(a, list(a), test=never_eq), (2, 0))

    def test_sequence_matcher(self):
        """Test the sequence matcher."""
        a = ["a", "b"]
        b = ["a", "b", "d", "c"]
        sm = SequenceMatcher(a=a, b=b)
        opcodes = [
            ["equal", 0, 1, 0, 1],
            ["equal", 1, 2, 1, 2],
            ["insert", 2, 2, 2, 3],
            ["insert", 2, 2, 3, 4],
        ]
        self.assertEqual(sm.distance(), 2)
        self.assertEqual(sm.ratio(), 2 / 3)
        self.assertEqual(sm.quick_ratio(), 2 / 3)
        self.assertEqual(sm.real_quick_ratio(), 2 / 3)
        self.assertEqual(sm.distance(), 2)
        # This doesn't return anything, saves the value in the sm cache.
        self.assertTrue(not sm._compute_distance_fast())
        self.assertEqual(sm.get_opcodes(), opcodes)
        self.assertEqual(list(sm.get_matching_blocks()), [[0, 0, 1], [1, 1, 1]])

    def test_sequence_matcher2(self):
        """Test the sequence matcher."""
        a = ["a", "b"]
        b = ["a", "b", "d", "c"]
        sm = SequenceMatcher()
        sm.set_seq1(a)
        sm.set_seq2(b)
        self.assertEqual(sm.distance(), 2)
        sm.set_seqs(b, a)
        self.assertEqual(sm.distance(), 2)

    def test_unsupported(self):
        """
        Test if calling unimplemented methods actually generates an error.
        """
        a = ["a", "b"]
        b = ["a", "b", "d", "c"]
        sm = SequenceMatcher(a=a, b=b)
        with self.assertRaises(NotImplementedError):
            sm.find_longest_match(1, 2, 3, 4)
        with self.assertRaises(NotImplementedError):
            sm.get_grouped_opcodes()

    def test_issue4_simpler(self):
        """Test for error reported here:
        https://github.com/belambert/edit-distance/issues/4"""
        a = ["that", "continuous", "sanction", ":=", "("]
        b = ["continuous", ":=", "(", "sanction", "^"]
        sm = SequenceMatcher(a=a, b=b)
        self.assertEqual(sm.distance(), 4)
        target_opcodes = [
            ["delete", 0, 1, 0, 0],
            ["equal", 1, 2, 0, 1],
            ["delete", 2, 3, 1, 1],
            ["equal", 3, 4, 1, 2],
            ["equal", 4, 5, 2, 3],
            ["insert", 5, 5, 3, 4],
            ["insert", 5, 5, 4, 5],
        ]
        self.assertEqual(sm.get_opcodes(), target_opcodes)

    def test_issue4(self):
        """Test for error reported here:
        https://github.com/belambert/edit-distance/issues/4"""
        a = [
            "that",
            "continuous",
            "sanction",
            ":=",
            "(",
            "flee",
            "U",
            "complain",
            ")",
            "E",
            "attendance",
            "eye",
            "^",
            "flowery",
            "revelation",
            "^",
            "ridiculous",
            "destination",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
        ]  # noqa
        b = [
            "continuous",
            ":=",
            "(",
            "sanction",
            "^",
            "flee",
            "^",
            "attendance",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
            "<EOS>",
        ]  # noqa
        target_opcodes = [
            ["delete", 0, 1, 0, 0],
            ["equal", 1, 2, 0, 1],
            ["delete", 2, 3, 1, 1],
            ["equal", 3, 4, 1, 2],
            ["equal", 4, 5, 2, 3],
            ["insert", 5, 5, 3, 4],
            ["insert", 5, 5, 4, 5],
            ["equal", 5, 6, 5, 6],
            ["replace", 6, 7, 6, 7],
            ["replace", 7, 8, 7, 8],
            ["replace", 8, 9, 8, 9],
            ["replace", 9, 10, 9, 10],
            ["replace", 10, 11, 10, 11],
            ["replace", 11, 12, 11, 12],
            ["replace", 12, 13, 12, 13],
            ["replace", 13, 14, 13, 14],
            ["replace", 14, 15, 14, 15],
            ["replace", 15, 16, 15, 16],
            ["replace", 16, 17, 16, 17],
            ["replace", 17, 18, 17, 18],
            ["equal", 18, 19, 18, 19],
            ["equal", 19, 20, 19, 20],
            ["equal", 20, 21, 20, 21],
            ["equal", 21, 22, 21, 22],
            ["equal", 22, 23, 22, 23],
            ["equal", 23, 24, 23, 24],
            ["equal", 24, 25, 24, 25],
            ["equal", 25, 26, 25, 26],
            ["equal", 26, 27, 26, 27],
            ["equal", 27, 28, 27, 28],
            ["equal", 28, 29, 28, 29],
        ]  # noqa
        sm = SequenceMatcher(a=a, b=b)
        self.assertEqual(sm.distance(), 16)
        self.assertEqual(sm.get_opcodes(), target_opcodes)

    def test_issue13(self):
        sm = SequenceMatcher(a="abc", b="abdc")
        self.assertEqual(
            [
                ["equal", 0, 1, 0, 1],
                ["equal", 1, 2, 1, 2],
                ["insert", 2, 2, 2, 3],
                ["equal", 2, 3, 3, 4],
            ],
            sm.get_opcodes(),
        )
