from __future__ import division

import unittest

from edit_distance import edit_distance_backpointer
from edit_distance import edit_distance
from edit_distance import highest_match_action
from edit_distance import SequenceMatcher

class TestEditDistance(unittest.TestCase):

    def test_edit_distance1(self):
        a = ['a', 'b']
        b = ['a', 'c', 'd', 'a', 'b']
        assert(edit_distance(a, b) == (3, 2))
        bp_expected_result = (3, 2, [['insert', 0, 0, 0, 1],
                                     ['insert', 0, 0, 1, 2],
                                     ['insert', 0, 0, 2, 3],
                                     ['equal', 0, 1, 3, 4],
                                     ['equal', 1, 2, 4, 5]])
        assert(edit_distance_backpointer(a, b) == bp_expected_result)

    def test_edit_distance2(self):
        a = ['hi', 'my', 'name', 'is', 'andy']
        b = ['hi', "i'm", 'my', "name's", 'sandy']
        assert(edit_distance(a, b) == (4, 1))
        bp_expected_result = (4, 1, [['equal', 0, 1, 0, 1],
                                     ['replace', 1, 2, 1, 2],
                                     ['replace', 2, 3, 2, 3],
                                     ['replace', 3, 4, 3, 4],
                                     ['replace', 4, 5, 4, 5]])
        assert(edit_distance_backpointer(a, b) == bp_expected_result)

    def test_edit_distance_highest_match(self):
        a = ['hi', 'my', 'name', 'is', 'andy']
        b = ['hi', "i'm", 'my', "name's", 'sandy']
        assert(edit_distance(a, b, action_function=highest_match_action) == (4, 2))
        bp_expected_result = (4, 2, [['equal', 0, 1, 0, 1],
                                     ['insert', 0, 0, 1, 2],
                                     ['equal', 1, 2, 2, 3],
                                     ['delete', 2, 3, 2, 2],
                                     ['replace', 3, 4, 3, 4],
                                     ['replace', 4, 5, 4, 5]])
        assert(edit_distance_backpointer(a, b, action_function=highest_match_action) == bp_expected_result)
        
    def test_edit_distance3(self):
        a = ['are', 'you', 'at', 'work', 'now']
        b = ['i', 'feel', 'are', 'saying']
        bp_expected_result = (5, 0, [['delete', 0, 1, 0, 0],
                                     ['replace', 1, 2, 0, 1],
                                     ['replace', 2, 3, 1, 2],
                                     ['replace', 3, 4, 2, 3],
                                     ['replace', 4, 5, 3, 4]])
        assert(edit_distance_backpointer(a, b) == bp_expected_result)

    def test_edit_distance4(self):
        a = []
        b = ['a', 'c']
        assert(edit_distance(a, b) == (2, 0))
        assert(edit_distance(b, a) == (2, 0))
        assert(edit_distance(a, a) == (0, 0))


    def test_sequence_matcher(self):
        a = ['a', 'b']
        b = ['a', 'b', 'd', 'c']
        sm = SequenceMatcher(a=a, b=b)
        assert(sm.ratio() == 2/3)
        assert(sm.quick_ratio() == 2/3)
        assert(sm.real_quick_ratio() == 2/3)
        assert(sm.distance() == 2)
        assert(sm._compute_distance_fast() == None) # This doesn't return anything.  Just saves the value in a cache.
        assert(sm.get_opcodes() == [['equal', 0, 1, 0, 1], ['equal', 1, 2, 1, 2], ['insert', 1, 1, 2, 3], ['insert', 1, 1, 3, 4]])
        assert(list(sm.get_matching_blocks()) == [[0, 0, 1], [1, 1, 1]])

    # def test_unsupported(self):
    #     a = ['a', 'b']
    #     b = ['a', 'b', 'd', 'c']
    #     sm = SequenceMatcher(a=a, b=b)
    #     self.assertRaises(NotImplementedError, sm.find_longest_match(1, 2, 3, 4))
    #     self.assertRaises(NotImplementedError, sm.get_grouped_opcodes())
