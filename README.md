============
edit_distance
============

[![Build Status](https://travis-ci.org/belambert/edit-distance.svg?branch=master)](https://travis-ci.org/belambert/edit-distance)
[![PyPI version](https://badge.fury.io/py/Edit_Distance.svg)](https://badge.fury.io/py/Edit_Distance)
[![Coverage Status](https://coveralls.io/repos/github/belambert/edit-distance/badge.svg?branch=master)](https://coveralls.io/github/belambert/edit-distance?branch=master)

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
```bash
pip install edit_distance
```

Alternatively you can clone this git repo and install using distutils:
```bash
git clone git@github.com:belambert/edit_distance.git
cd edit_distance
python setup.py install
```

To uninstall with pip:
```bash
pip uninstall edit_distance
```

API usage
---------

To see examples of usage, view the [difflib documentation](http://docs.python.org/2/library/difflib.html).
Additional API-level documentation is available on [ReadTheDocs](http://edit-distance.readthedocs.io/en/latest/)

This requires Python 2.7+ since it uses argparse for the command line 
interface.  The rest of the code should be OK with earlier versions of Python

Example API usage:
```python
import edit_distance
ref = [1, 2, 3, 4]
hyp = [1, 2, 4, 5, 6]
sm = edit_distance.SequenceMatcher(a=ref, b=hyp)
sm.get_opcodes()
sm.ratio()
sm.get_matching_blocks()
```

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
