============
editdistance
============

Python module for computing edit distances and alignments between sequences.

I needed a way to compute edit distances between sequences in Python.  I wasn't able to find any appropriate libraries that do this so I wrote my own.  There appear to be numerous editdistance libraries available for computing edit distances between two strings, but not between two sequences.

I haven't been able to test this library for correctness yet.  If you can test/verify this, please do!  This is also written entirely in Python.  This implementation could likely be optimized to be faster within Python.  And could probably be *much* faster if implemented in C.

The library API is modeled after difflib.SequenceMatcher.  This is very similar to difflib, except that this module computes editdistance (Levenshtein distance) rather than the Ratcliff and Oberhelp method that Python's difflib uses.  difflib "does not yield minimal edit sequences, but does tend to yield matches that 'look right' to people."

If you find this library useful or have any comments/criticism, please send me a message!


Command line usage
------------------

For command line usage, see:

    python editdistance.py --help


API usage
---------

To see examples of usage, view the difflib documentation:
http://docs.python.org/2/library/difflib.html

This requires Python 2.7+ since it uses argparse for the command line interface.  The rest of the code should be OK with earlier versions of Python

Example API usage:

    import editdistance
    sm = editdistance.SequenceMatcher(a=ref, b=hyp)
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

    sm = editdistance.SequenceMatcher(a=ref, b=hyp, action_function=editdistance.highest_match_action)


Notes
-----

 * This doesn't implement the 'junk' matching stuff in difflib.




