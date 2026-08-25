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
int_pairs = st.tuples(ints, ints)


# Integer costs so the weighted assertions stay exact -- summing floats in a
# different order than the search did would make them flaky.  Insertions and
# deletions are priced differently so each boundary is exercised on its own,
# and substitutions sometimes cost more than a gap pair and sometimes less.
def sub_c(x, y):
    """Substitution cost: free for a match, otherwise 2 to 5."""
    return 0 if x == y else 2 + abs(x - y)


def ins_c(y):
    """Insertion cost: 1 to 4."""
    return 1 + y


def del_c(x):
    """Deletion cost: 2 to 5."""
    return 2 + x


WEIGHTED = {
    "substitution_cost": sub_c,
    "insertion_cost": ins_c,
    "deletion_cost": del_c,
}


def check_opcodes_tile(a, b, opcodes):
    """Opcodes tile the alignment from (0, 0) to (len(a), len(b)) and applying
    them to a yields b."""
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
def test_opcodes_contiguous_and_reconstruct(pair):
    """Opcodes tile the alignment from (0, 0) to (len(a), len(b)) and
    applying them to a yields b."""
    a, b = pair
    _, _, opcodes = edit_distance_backpointer(a, b)
    check_opcodes_tile(a, b, opcodes)


@given(int_pairs)
def test_weighted_opcodes_contiguous_and_reconstruct(pair):
    """Custom costs change which alignment wins, not the structural
    guarantees the opcodes have to satisfy."""
    a, b = pair
    _, _, opcodes = edit_distance_backpointer(a, b, **WEIGHTED)
    check_opcodes_tile(a, b, opcodes)


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


@given(int_pairs)
def test_weighted_agrees_with_wagner_fischer(pair):
    """Both entry points agree with a reference weighted Wagner-Fischer
    distance, whose boundary rows are cumulative sums of the gap costs."""
    a, b = pair
    expected = weighted_wagner_fischer(a, b)
    assert edit_distance(a, b, **WEIGHTED)[0] == expected
    assert edit_distance_backpointer(a, b, **WEIGHTED)[0] == expected


@given(int_pairs)
def test_weighted_distance_equals_summed_opcode_costs(pair):
    """The distance is exactly what the returned alignment costs.  This is the
    weighted generalization of counting non-equal opcodes."""
    a, b = pair
    dist, matches, opcodes = edit_distance_backpointer(a, b, **WEIGHTED)
    total = 0
    for tag, i1, _, j1, _ in opcodes:
        if tag in ("equal", "replace"):
            total += sub_c(a[i1], b[j1])
        elif tag == "insert":
            total += ins_c(b[j1])
        else:
            total += del_c(a[i1])
    assert total == dist
    assert (dist, matches) == edit_distance(a, b, **WEIGHTED)


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


def weighted_wagner_fischer(a, b):
    """Reference weighted distance using the full DP table.  Written
    independently of the implementation, including the boundary rows."""
    m, n = len(a), len(b)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        d[i][0] = d[i - 1][0] + del_c(a[i - 1])
    for j in range(1, n + 1):
        d[0][j] = d[0][j - 1] + ins_c(b[j - 1])
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            d[i][j] = min(
                d[i - 1][j] + del_c(a[i - 1]),
                d[i][j - 1] + ins_c(b[j - 1]),
                d[i - 1][j - 1] + sub_c(a[i - 1], b[j - 1]),
            )
    return d[m][n]
