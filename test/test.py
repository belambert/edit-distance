# Copyright 2013-2018 Ben Lambert

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
from __future__ import division

import unittest

from edit_distance import edit_distance_backpointer
from edit_distance import edit_distance
from edit_distance import highest_match_action
from edit_distance import SequenceMatcher

class TestEditDistance(unittest.TestCase):
    """Class to hold all the tests for this package."""

    def test_edit_distance1(self):
        """Test edit distance between 'ab' and 'acdab'."""
        a = ['a', 'b']
        b = ['a', 'c', 'd', 'a', 'b']
        self.assertTrue(edit_distance(a, b) == (3, 2))
        bp_expected_result = (3, 2, [['insert', 0, 0, 0, 1],
                                     ['insert', 0, 0, 1, 2],
                                     ['insert', 0, 0, 2, 3],
                                     ['equal', 0, 1, 3, 4],
                                     ['equal', 1, 2, 4, 5]])
        self.assertTrue(edit_distance_backpointer(a, b) == bp_expected_result)

    def test_edit_distance2(self):
        """Test edit distance for 'hi my name is andy'."""
        a = ['hi', 'my', 'name', 'is', 'andy']
        b = ['hi', "i'm", 'my', "name's", 'sandy']
        self.assertTrue(edit_distance(a, b) == (4, 1))
        bp_expected_result = (4, 1, [['equal', 0, 1, 0, 1],
                                     ['replace', 1, 2, 1, 2],
                                     ['replace', 2, 3, 2, 3],
                                     ['replace', 3, 4, 3, 4],
                                     ['replace', 4, 5, 4, 5]])
        self.assertTrue(edit_distance_backpointer(a, b) == bp_expected_result)

    def test_edit_distance_highest_match(self):
        """Test edit distance for 'hi my name is andy', maximizing matches rather than
        minimizing edits."""
        a = ['hi', 'my', 'name', 'is', 'andy']
        b = ['hi', "i'm", 'my', "name's", 'sandy']
        self.assertTrue(edit_distance(a, b, action_function=highest_match_action) == (4, 2))
        bp_expected_result = (4, 2, [['equal', 0, 1, 0, 1],
                                     ['insert', 0, 0, 1, 2],
                                     ['equal', 1, 2, 2, 3],
                                     ['delete', 2, 3, 2, 2],
                                     ['replace', 3, 4, 3, 4],
                                     ['replace', 4, 5, 4, 5]])
        self.assertTrue(edit_distance_backpointer(a, b, action_function=highest_match_action) == bp_expected_result)

    def test_edit_distance3(self):
        """Test for 'are you at work now'."""
        a = ['are', 'you', 'at', 'work', 'now']
        b = ['i', 'feel', 'are', 'saying']
        bp_expected_result = (5, 0, [['delete', 0, 1, 0, 0],
                                     ['replace', 1, 2, 0, 1],
                                     ['replace', 2, 3, 1, 2],
                                     ['replace', 3, 4, 2, 3],
                                     ['replace', 4, 5, 3, 4]])
        self.assertTrue(edit_distance_backpointer(a, b) == bp_expected_result)

    def test_edit_distance4(self):
        """Test edit distance against an empty list."""
        a = []
        b = ['a', 'c']
        self.assertTrue(edit_distance(a, b) == (2, 0))
        self.assertTrue(edit_distance(b, a) == (2, 0))
        self.assertTrue(edit_distance(a, a) == (0, 0))

    def test_sequence_matcher(self):
        """Test the sequence matcher."""
        a = ['a', 'b']
        b = ['a', 'b', 'd', 'c']
        sm = SequenceMatcher(a=a, b=b)
        opcodes = [['equal', 0, 1, 0, 1], ['equal', 1, 2, 1, 2], ['insert', 1, 1, 2, 3], ['insert', 1, 1, 3, 4]]
        self.assertTrue(sm.distance() == 2)
        self.assertTrue(sm.ratio() == 2 / 3)
        self.assertTrue(sm.quick_ratio() == 2 / 3)
        self.assertTrue(sm.real_quick_ratio() == 2 / 3)
        self.assertTrue(sm.distance() == 2)
        # This doesn't return anything, saves the value in the sm cache.
        self.assertTrue(not sm._compute_distance_fast())
        self.assertTrue(sm.get_opcodes() == opcodes)
        self.assertTrue(list(sm.get_matching_blocks()) == [[0, 0, 1], [1, 1, 1]])

    def test_sequence_matcher2(self):
        """Test the sequence matcher."""
        a = ['a', 'b']
        b = ['a', 'b', 'd', 'c']
        sm = SequenceMatcher()
        sm.set_seq1(a)
        sm.set_seq2(b)
        self.assertTrue(sm.distance() == 2)
        sm.set_seqs(b, a)
        self.assertTrue(sm.distance() == 2)

    def test_unsupported(self):
        """Test if calling unimplemented methods actually generates an error."""
        a = ['a', 'b']
        b = ['a', 'b', 'd', 'c']
        sm = SequenceMatcher(a=a, b=b)
        with self.assertRaises(NotImplementedError):
            sm.find_longest_match(1, 2, 3, 4)
        with self.assertRaises(NotImplementedError):
            sm.get_grouped_opcodes()

    def test_issue4_simpler(self):
        """ Test for error reported here:
        https://github.com/belambert/edit-distance/issues/4 """
        a = ['that', 'continuous', 'sanction', ':=', '(']
        b = ['continuous', ':=', '(', 'sanction', '^']
        sm = SequenceMatcher(a=a, b=b)
        self.assertEqual(sm.distance(),  4)
        target_opcodes = [['delete', 0, 1, 0, 0], ['equal', 1, 2, 0, 1], ['delete', 2, 3, 0, 0], ['equal', 3, 4, 1, 2], ['equal', 4, 5, 2, 3], ['insert', 4, 4, 3, 4], ['insert', 4, 4, 4, 5]]
        self.assertEqual(sm.get_opcodes(), target_opcodes)

    def test_issue4(self):
        """ Test for error reported here:
        https://github.com/belambert/edit-distance/issues/4 """
        a = ['that', 'continuous', 'sanction', ':=', '(', 'flee', 'U', 'complain', ')', 'E', 'attendance', 'eye', '^', 'flowery', 'revelation', '^', 'ridiculous', 'destination', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>']
        b = ['continuous', ':=', '(', 'sanction', '^', 'flee', '^', 'attendance', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>', '<EOS>']
        target_opcodes = [['delete', 0, 1, 0, 0], ['equal', 1, 2, 0, 1], ['delete', 2, 3, 0, 0], ['equal', 3, 4, 1, 2], ['equal', 4, 5, 2, 3], ['insert', 4, 4, 3, 4], ['insert', 4, 4, 4, 5], ['equal', 5, 6, 5, 6], ['replace', 6, 7, 6, 7], ['replace', 7, 8, 7, 8], ['replace', 8, 9, 8, 9], ['replace', 9, 10, 9, 10], ['replace', 10, 11, 10, 11], ['replace', 11, 12, 11, 12], ['replace', 12, 13, 12, 13], ['replace', 13, 14, 13, 14], ['replace', 14, 15, 14, 15], ['replace', 15, 16, 15, 16], ['replace', 16, 17, 16, 17], ['replace', 17, 18, 17, 18], ['equal', 18, 19, 18, 19], ['equal', 19, 20, 19, 20], ['equal', 20, 21, 20, 21], ['equal', 21, 22, 21, 22], ['equal', 22, 23, 22, 23], ['equal', 23, 24, 23, 24], ['equal', 24, 25, 24, 25], ['equal', 25, 26, 25, 26], ['equal', 26, 27, 26, 27], ['equal', 27, 28, 27, 28], ['equal', 28, 29, 28, 29]]
        sm = SequenceMatcher(a=a, b=b)
        self.assertEqual(sm.distance(), 16)
        self.assertEqual(sm.get_opcodes(), target_opcodes)
