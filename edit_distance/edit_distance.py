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
Code for computing edit distances.
"""

import operator
import sys
from collections.abc import Callable, Sequence
from typing import Any

INSERT: str = "insert"
DELETE: str = "delete"
EQUAL: str = "equal"
REPLACE: str = "replace"

TestFunction = Callable[[Any, Any], Any]
SubstitutionCostFunction = Callable[[Any, Any], float]
GapCostFunction = Callable[[Any], float]


# At each cell the search takes whichever of the three actions is cheapest,
# breaking ties in favor of substitution, then insertion, then deletion.
#
# Two properties of custom costs are worth knowing:
#
# * A substitution costing more than an insertion plus a deletion is never
#   chosen -- the search routes around it by deleting and then inserting -- so
#   substitution costs are effectively capped at ``ins + del``.
# * ``distance(a, a) == 0`` only holds if a match costs nothing, and symmetry
#   only holds if insertions and deletions cost the same.  Keeping the result a
#   true metric is the caller's responsibility.


def edit_distance(
    seq1: Sequence,
    seq2: Sequence,
    *,
    test: TestFunction = operator.eq,
    substitution_cost: SubstitutionCostFunction | None = None,
    insertion_cost: GapCostFunction | None = None,
    deletion_cost: GapCostFunction | None = None,
) -> tuple[float, int]:
    """
    Computes the edit distance between the two given sequences.  This uses the
    relatively fast method that only constructs two columns of the 2d array
    for edits.  This function actually uses four columns because we track the
    number of matches too.  Returns a ``(distance, matches)`` tuple.

    ``test`` decides whether two elements are equal.  It governs the opcode
    label (``equal`` versus ``replace``) and the match count, and defaults to
    :py:func:`operator.eq`.

    The three cost functions decide only what each operation *costs*:

    * ``substitution_cost(x, y)`` -- the cost of aligning ``x`` with ``y``.
      This is consulted for **every** aligned pair, including pairs that
      ``test`` considers equal, so a custom function must handle both cases;
      the usual form is ``lambda x, y: 0 if x == y else penalty(x, y)``.
      Defaults to ``0`` for a match and ``1`` otherwise.
    * ``insertion_cost(y)`` -- the cost of inserting ``y``.  Defaults to ``1``.
    * ``deletion_cost(x)`` -- the cost of deleting ``x``.  Defaults to ``1``.

    Costs and equality are independent: a zero-cost pair that ``test`` rejects
    is still a ``replace`` and does not count as a match, and a nonzero-cost
    pair that ``test`` accepts is still an ``equal`` and does.
    """
    m = len(seq1)
    n = len(seq2)
    # Identical sequences are only free when a match costs nothing, which a
    # custom substitution cost is under no obligation to honor.
    if substitution_cost is None and test is operator.eq and seq1 == seq2:
        return 0, n

    # Insertion costs are needed once per row, so pay for them only once.
    ins_costs = [1] * n if insertion_cost is None else [insertion_cost(y) for y in seq2]

    v0: list[float] = [0] * (n + 1)  # The two 'error' columns
    v1: list[float] = [0] * (n + 1)
    m0 = [0] * (n + 1)  # The two 'match' columns
    m1 = [0] * (n + 1)

    # The first row: the running cost of inserting all of seq2 up to here.
    for j in range(1, n + 1):
        v0[j] = v0[j - 1] + ins_costs[j - 1]
    if m == 0:
        return v0[n], 0

    for i in range(1, m + 1):
        a_elem = seq1[i - 1]
        elem_del_cost = 1 if deletion_cost is None else deletion_cost(a_elem)
        # The first column: the running cost of deleting all of seq1 up to here.
        v1[0] = v0[0] + elem_del_cost
        for j in range(1, n + 1):
            b_elem = seq2[j - 1]
            equal = test(a_elem, b_elem)
            if substitution_cost is None:
                cost: float = 0 if equal else 1
            else:
                cost = substitution_cost(a_elem, b_elem)
            # The costs
            ins_cost = v1[j - 1] + ins_costs[j - 1]
            del_cost = v0[j] + elem_del_cost
            sub_cost = v0[j - 1] + cost
            # Match counts
            ins_match = m1[j - 1]
            del_match = m0[j]
            sub_match = m0[j - 1] + (1 if equal else 0)

            # Ties break in favor of substitution, then insertion, then deletion.
            if sub_cost <= ins_cost and sub_cost <= del_cost:
                v1[j] = sub_cost
                m1[j] = sub_match
            elif ins_cost <= del_cost:
                v1[j] = ins_cost
                m1[j] = ins_match
            else:
                v1[j] = del_cost
                m1[j] = del_match
        # Copy the columns over
        for k in range(n + 1):
            v0[k] = v1[k]
            m0[k] = m1[k]
    return v1[n], m1[n]


def edit_distance_backpointer(
    seq1: Sequence,
    seq2: Sequence,
    *,
    test: TestFunction = operator.eq,
    substitution_cost: SubstitutionCostFunction | None = None,
    insertion_cost: GapCostFunction | None = None,
    deletion_cost: GapCostFunction | None = None,
) -> tuple[float, int, list]:
    """
    Similar to :py:func:`~edit_distance.edit_distance` except that this
    function keeps backpointers during the search.  This allows us to return
    the opcodes (i.e. the specific edits that were used to change from one
    string to another).  This function contructs the full 2d array for the
    backpointers only.  Returns a ``(distance, matches, opcodes)`` tuple.

    ``test`` and the three cost functions mean the same thing they do for
    :py:func:`~edit_distance.edit_distance`.
    """
    m: int = len(seq1)
    n: int = len(seq2)
    # backpointer array:
    bp: list[list[str | None]] = [[None for _ in range(n + 1)] for _ in range(m + 1)]

    # Insertion costs are needed once per row, so pay for them only once.
    ins_costs = [1] * n if insertion_cost is None else [insertion_cost(y) for y in seq2]

    # Two columns of the distance and match arrays
    d0: list[float] = [0] * (n + 1)  # The two 'distance' columns
    d1: list[float] = [0] * (n + 1)
    m0 = [0] * (n + 1)  # The two 'match' columns
    m1 = [0] * (n + 1)

    # Fill in the first row: the running cost of inserting all of seq2.
    for j in range(1, n + 1):
        d0[j] = d0[j - 1] + ins_costs[j - 1]
        bp[0][j] = INSERT

    for i in range(1, m + 1):
        a_elem = seq1[i - 1]
        elem_del_cost = 1 if deletion_cost is None else deletion_cost(a_elem)
        # The first column: the running cost of deleting all of seq1 up to here.
        d1[0] = d0[0] + elem_del_cost
        bp[i][0] = DELETE

        for j in range(1, n + 1):
            b_elem = seq2[j - 1]
            equal = test(a_elem, b_elem)
            if substitution_cost is None:
                cost: float = 0 if equal else 1
            else:
                cost = substitution_cost(a_elem, b_elem)
            # The costs of each action...
            ins_cost = d1[j - 1] + ins_costs[j - 1]  # insertion
            del_cost = d0[j] + elem_del_cost  # deletion
            sub_cost = d0[j - 1] + cost  # substitution/match

            # The match scores of each action
            ins_match = m1[j - 1]
            del_match = m0[j]
            sub_match = m0[j - 1] + (1 if equal else 0)

            # Ties break in favor of substitution, then insertion, then deletion.
            if sub_cost <= ins_cost and sub_cost <= del_cost:
                d1[j] = sub_cost
                m1[j] = sub_match
                bp[i][j] = EQUAL if equal else REPLACE
            elif ins_cost <= del_cost:
                d1[j] = ins_cost
                m1[j] = ins_match
                bp[i][j] = INSERT
            else:
                d1[j] = del_cost
                m1[j] = del_match
                bp[i][j] = DELETE
        # copy over the columns
        for k in range(n + 1):
            d0[k] = d1[k]
            m0[k] = m1[k]
    opcodes = get_opcodes_from_bp_table(bp)
    # d0/m0 hold the final column even when seq1 is empty and the loop never runs
    return d0[n], m0[n], opcodes


def get_opcodes_from_bp_table(bp):
    """Given a 2d list structure, create opcodes from the best path."""
    x = len(bp) - 1
    y = len(bp[0]) - 1
    opcodes = []
    while x != 0 or y != 0:
        this_bp = bp[x][y]
        if this_bp in [EQUAL, REPLACE]:
            opcodes.append([this_bp, x - 1, x, y - 1, y])
            x = x - 1
            y = y - 1
        elif this_bp == INSERT:
            opcodes.append([INSERT, x, x, y - 1, y])
            y = y - 1
        elif this_bp == DELETE:
            opcodes.append([DELETE, x - 1, x, y, y])
            x = x - 1
        else:
            raise Exception("Invalid dynamic programming action in BP table!")
    opcodes.reverse()
    return opcodes


def main() -> int:
    """Read two files line-by-line and print edit distances between each pair
    of lines. Will terminate at the end of the shorter of the two files."""

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file1> <file2>")
        sys.exit(-1)
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    with open(file1) as f1, open(file2) as f2:
        for line1, line2 in zip(f1, f2):
            print(f"Line 1: {line1.strip()}")
            print(f"Line 2: {line2.strip()}")
            dist, _, _ = edit_distance_backpointer(line1.split(), line2.split())
            print(f"Distance: {dist}")
            print("=" * 80)
    return 0


if __name__ == "__main__":
    main()
