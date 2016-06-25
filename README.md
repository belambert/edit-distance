============
edit_distance
============

Python module for computing edit distances and alignments between sequences.

I needed a way to compute edit distances between sequences in Python.  I wasn't
able to find any appropriate libraries that do this so I wrote my own.  There
appear to be numerous edit distance libraries available for computing edit
distances between two strings, but not between two sequences.

This is also written entirely in Python.  This implementation could likely be
optimized to be faster within Python.  And could probably be much faster if
implemented in C.

The library API is modeled after difflib.SequenceMatcher.  This is very similar
to difflib, except that this module computes edit distance (Levenshtein distance)
rather than the Ratcliff and Oberhelp method that Python's difflib uses.  difflib
"does not yield minimal edit sequences, but does tend to yield matches that
'look right' to people."

If you find this library useful or have any suggestions, please send me a
message.


Installing & uninstalling
-------------------------

The easiest way to install is using pip:

    pip install edit_distance

Alternatively you can clone this git repo and install using distutils:

    git clone git@github.com:belambert/edit_distance.git
    cd edit_distance
    python setup.py install

To uninstall with pip:

    pip uninstall edit_distance


Command line usage
------------------

For command line usage, see:

    python edit_distance.py --help


API usage
---------

To see examples of usage, view the difflib documentation:
http://docs.python.org/2/library/difflib.html

This requires Python 2.7+ since it uses argparse for the command line interface.  The rest of the code should be OK with earlier versions of Python

Example API usage:

    import edit_distance
    sm = edit_distance.SequenceMatcher(a=ref, b=hyp)
    sm.get_opcodes()
    sm.ratio()
    sm.get_matching_blocks()


Differences from difflib
------------------------

In addition to the SequenceMatcher methods, distance() and matches() methods are provided which compute the edit distance and the number of matches.

    sm.distance()
    sm.matches()

Even if the alignment of the two sequences is identical to difflib, get_opcodes() and get_matching_blocks() may return slightly different sequences.  The opcodes returned by this library represent individual character operations, and thus should never span two or more characters.

It's also possible to compute the maximum number of matches rather than the minimum number of edits:

    sm = edit_distance.SequenceMatcher(a=ref, b=hyp, action_function=edit_distance.highest_match_action)

Notes
-----

 * This doesn't implement the 'junk' matching features in difflib.
