============
editdistance
============

Python module for computing edit distances and alignments between sequences.

The library API is modeled after difflib.SequenceMatcher.  This is very similar to difflib, except that this module computes editdistance (Levenshtein distance) rather than the Ratcliff and Oberhelp method that Python's difflib uses.  difflib "does not yield minimal edit sequences, but does tend to yield matches that 'look right' to people."

Command line usage
==================

For command line usage, see:
python editdistance.py --help

API usage
=========

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
========================

In addition to the SequenceMatcher methods, distance() and matches() methods are provided which compute the edit distance and the number of matches.

Even if the alignment of the two sequences is identical to difflib, get_opcodes() and get_matching_blocks() may return slightly different sequences.

It's also possible to compute the maximum number of matches...
sm = editdistance.SequenceMatcher(a=ref, b=hyp, action_function=editdistance.highest_match_action)