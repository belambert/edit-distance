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
Property-based tests for edit_distance using hypothesis.
"""
from hypothesis import given
from hypothesis import strategies as st

from edit_distance import edit_distance, edit_distance_backpointer

# Small alphabets so generated pairs frequently share elements.
ints = st.lists(st.integers(0, 3), max_size=10)
strs = st.text("abc", max_size=10)
seqs = ints | strs
pairs = st.tuples(ints, ints) | st.tuples(strs, strs)


@given(pairs)
def test_opcodes_contiguous_and_reconstruct(pair):
    """Opcodes tile the alignment from (0, 0) to (len(a), len(b)) and
    applying them to a yields b."""
    a, b = pair
    _, _, opcodes = edit_distance_backpointer(a, b)

    pos = (0, 0)
    out = []
    for tag, i1, i2, j1, j2 in opcodes:
        assert (i1, j1) == pos
        if tag == "equal":
            assert list(a[i1:i2]) == list(b[j1:j2])
            out.extend(a[i1:i2])
        elif tag in ("replace", "insert"):
            out.extend(b[j1:j2])
        else:
            assert tag == "delete"
        pos = (i2, j2)

    assert pos == (len(a), len(b))
    assert out == list(b)


@given(pairs)
def test_distance_counts_non_equal_opcodes(pair):
    """The distance equals the number of non-equal opcodes and agrees with
    edit_distance."""
    a, b = pair
    dist, matches, opcodes = edit_distance_backpointer(a, b)
    assert dist == sum(1 for op in opcodes if op[0] != "equal")
    assert (dist, matches) == edit_distance(a, b)


@given(pairs)
def test_symmetry(pair):
    """distance(a, b) == distance(b, a)."""
    a, b = pair
    assert edit_distance(a, b)[0] == edit_distance(b, a)[0]


@given(seqs)
def test_identity(a):
    """distance(a, a) == 0."""
    assert edit_distance(a, a)[0] == 0


@given(pairs)
def test_bounds(pair):
    """abs(len(a) - len(b)) <= distance <= max(len(a), len(b))."""
    a, b = pair
    dist = edit_distance(a, b)[0]
    assert abs(len(a) - len(b)) <= dist <= max(len(a), len(b))


@given(pairs)
def test_agrees_with_wagner_fischer(pair):
    """Both entry points agree with a reference Wagner-Fischer distance."""
    a, b = pair
    expected = wagner_fischer(a, b)
    assert edit_distance(a, b)[0] == expected
    assert edit_distance_backpointer(a, b)[0] == expected


def wagner_fischer(a, b):
    """Reference Levenshtein distance using the full DP table."""
    m, n = len(a), len(b)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
    return d[m][n]
