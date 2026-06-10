edit_distance
=============
[![build](https://github.com/belambert/edit-distance/actions/workflows/build.yml/badge.svg)](https://github.com/belambert/edit-distance/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/Edit_Distance.svg)](https://badge.fury.io/py/Edit_Distance)
[![codecov](https://codecov.io/gh/belambert/edit-distance/branch/main/graph/badge.svg?token=43c8bYhWeL)](https://codecov.io/gh/belambert/edit-distance)

Python module for computing edit distances and alignments between sequences.

I needed a way to compute edit distances between sequences in Python.  I wasn't
able to find any appropriate libraries that do this so I wrote my own.  There
appear to be numerous edit distance libraries available for computing edit
distances between two strings, but not between two sequences.

This is written entirely in Python.  This implementation could likely be
optimized to be faster within Python.  And could probably be much faster if
implemented in C.

The library API is modeled after difflib.SequenceMatcher.  This is very similar
to difflib, except that this module computes edit distance (Levenshtein 
distance) rather than the Ratcliff and Oberhelp method that Python's difflib
uses. difflib "does not yield minimal edit sequences, but does tend to yield
matches that 'look right' to people."

If you find this library useful or have any suggestions, please send me a
message.

Installing & uninstalling
-------------------------
The easiest way to install is using pip:

    pip install edit_distance

To uninstall with pip:

    pip uninstall edit_distance

This requires Python 3.9 or later.

API usage
---------
To see examples of usage, view the [difflib documentation](https://docs.python.org/3/library/difflib.html).
Additional API-level documentation is available on [ReadTheDocs](http://edit-distance.readthedocs.io/en/latest/)

Example API usage:

```python
import edit_distance
ref = ["hi", "there", "how", "are", "you"]
hyp = ["hi", "here", "how", "are", "you", "doing"]
sm = edit_distance.SequenceMatcher(a=ref, b=hyp)

sm.distance()
# 2
sm.get_opcodes()
# [['equal', 0, 1, 0, 1], ['replace', 1, 2, 1, 2], ['equal', 2, 3, 2, 3], ['equal', 3, 4, 3, 4], ['equal', 4, 5, 4, 5], ['insert', 5, 5, 5, 6]]
list(sm.get_matching_blocks())
# [[0, 0, 1], [2, 2, 1], [3, 3, 1], [4, 4, 1]]
sm.ratio()
# 0.7272727272727273
```

Command line usage
------------------
Installing the package also installs an `edit-distance` command, which compares
two files line by line and prints the edit distance between each pair of lines:

    edit-distance file1.txt file2.txt

Differences from difflib
------------------------
In addition to the `SequenceMatcher` methods, `distance()` and `matches()` methods 
are provided which compute the edit distance and the number of matches.

```python
sm.distance()
sm.matches()
```

Even if the alignment of the two sequences is identical to `difflib`, 
`get_opcodes()` and `get_matching_blocks()` may return slightly different 
sequences.  The opcodes returned by this library represent individual character 
operations, and thus should never span two or more characters.

It's also possible to compute the maximum number of matches rather than the 
minimum number of edits:

```python
sm = edit_distance.SequenceMatcher(a=ref, b=hyp, 
     action_function=edit_distance.highest_match_action)
```

Notes
-----
This doesn't implement the 'junk' matching features in difflib.


Hacking
-------
To run unit tests:

    python -m unittest

To deploy...


Contributing and code of conduct
--------------------------------
For contributions, it's best to Github issues and pull requests. Proper
testing and documentation required.

Code of conduct is expected to be reasonable, especially as specified by
the [Contributor Covenant](http://contributor-covenant.org/version/1/4/)
