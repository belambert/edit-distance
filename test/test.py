import unittest

from edit_distance import edit_distance
from edit_distance import edit_distance_backpointer


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

    def test_edit_distance1(self):
        a = ['hi', 'my', 'name', 'is', 'andy']
        b = ['hi', "i'm", 'my', "name's", 'sandy']
        assert(edit_distance(a, b) == (4, 2))
        bp_expected_result = (4, 2, [['equal', 0, 1, 0, 1],
                                     ['insert', 0, 0, 1, 2],
                                     ['equal', 1, 2, 2, 3],
                                     ['delete', 2, 3, 2, 2],
                                     ['replace', 3, 4, 3, 4],
                                     ['replace', 4, 5, 4, 5]])
        assert(edit_distance_backpointer(a, b) == bp_expected_result)

    def test_edit_distance1(self):
        a = ['are', 'you', 'at', 'work', 'now']
        b = ['i', 'feel', 'are', 'saying']
        bp_expected_result = (5, 0, [['delete', 0, 1, 0, 0],
                                     ['replace', 1, 2, 0, 1],
                                     ['replace', 2, 3, 1, 2],
                                     ['replace', 3, 4, 2, 3],
                                     ['replace', 4, 5, 3, 4]])
        assert(edit_distance_backpointer(a, b) == bp_expected_result)
