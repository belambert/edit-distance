edit-distance's documentation
=========================================

.. toctree::
   :maxdepth: 2

.. py:module:: edit_distance

It is suggested to use either the function :py:func:`edit_distance` or the :py:class:`SequenceMatcher` class.

Functions
_________
.. autofunction:: edit_distance
.. autofunction:: edit_distance_backpointer

SequenceMatcher class
_____________________
.. autoclass:: SequenceMatcher
   :members:
   :special-members:

Match functions
_______________
These functions can be used to toggle whether we're minimizing edits
or maximizing matches.

.. autofunction:: lowest_cost_action
.. autofunction:: highest_match_action
 
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

