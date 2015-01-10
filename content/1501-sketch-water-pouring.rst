A water pouring problem sketched in Python
##########################################

:date: 2015-01-09 10:00
:category: Code
:summary: A small Python 3 sketch of a solution to a water pouring problem.
:scm_path: content/1501-sketch-water-pouring.rst

The problem
===========

At the end of last year, I came across the following water pouring problem
because something similar had come up in a friend's functional programming
interview:

    **There are three glasses on the table - 3, 5, and 8 oz. The first two are
    empty, the last contains 8 oz of water. By pouring water from one glass to
    another make at least one of them contain exactly 4 oz of water.**

*Source: A. Bogomolny,* `3 Glasses Puzzle from Interactive Mathematics
Miscellany and Puzzles <http://www.cut-the-knot.org/water.shtml>`_, *Accessed
09 January 2015*

A solution using search, not algebra
====================================

At first I started to explore the problem by looking at it algebraically. What
are the differences between each cup? How can those differences be summed
together to give the required remainder of 4?

However this didn't yield anything helpful. Instead, I started looking at the
solution states. What do the cups have to look like for the puzzle to be
solved?

Two success states
------------------

There are at least two success states. One where the 5 oz cup contains 4 oz
of water and the other where the 8 oz cup contains 4 oz of water. The other two
cups must contain the remaining 4 oz of water. This is the notation I've used
for these two states, where ``x + y = 4``:

::

    [<Cup x/3>, <Cup 4/5>, <Cup y/8>]

And:

::

    [<Cup x/3>, <Cup y/5>, <Cup 4/8>]

The search problem
------------------

So taking the second state, and assuming that the first cup is full, then the
question becomes:

    How do we get from the start state to the end state?

::

    [<Cup 0/3>, <Cup 0/5>, <Cup 8/8>]
    ...
    TODO: Search in here for a path
    ...
    [<Cup 3/3>, <Cup 1/5>, <Cup 4/8>]

This is really helpful. It turns an algebra problem into a search problem.
Computers are good at doing search. We can write code for this.


A Python 3 sketch
=================

I've written some Python to solve this problems using a type of depth first
`Tree Traversal <http://en.wikipedia.org/wiki/Tree_traversal>`_ and tree
generation strategy.

The `code repository is available on GitHub
<https://github.com/jamescooke/water-pouring-python>`_. The README contains the
installation and operating instructions.

These are some of the features of the code:

Cup and Game classes
--------------------

In this code, the `Cup
class <https://github.com/jamescooke/water-pouring-python/blob/master/water/cup.py>`_
represents a cup in the problem. Each Cup has a certain ``capacity`` and
``contents``. The benefit of using a Cup class as a data type is that it can
perform checks that is not holding more than its capacity of water or that it's
holding a negative capacity of water either.

The `Game
class <https://github.com/jamescooke/water-pouring-python/blob/master/water/game.py>`_
is more complex as it represents a single state in the tree. Each Game state
has three main properties:

* ``cups`` - The three Cups that make up this Game state.
* ``parent`` - The Game that came before this one in the search. The starting
  state will have this as ``None``, but all the rest will have a parent.
* ``children`` - Each Game will have some or no child Game states stored in a
  list. These are the valid states that can be made by pouring some or all of
  one Cup's contents into another Cup in the Game that haven't already been
  seen during the search.

The Game's ``children`` property makes the Game class a `recursive data
structure <http://en.wikipedia.org/wiki/Recursive_data_type>`_ because it can
contain other instances of Games. This opens the door to the recursive search
described below.

Again using this Game type is really helpful because I've been able to write
tested functions for supporting data type functions like ``__eq__`` (which
tests if two Game stats are logically the same). The most important function in
Game is ``is_solvable`` which implements the search function.

Recursive search
----------------

As mentioned above, the ``Game.is_solvable`` function implements the tree
search, so here it is in full, comments removed.

.. code-block:: python

    def is_solvable(self):
        if self.is_goal():
            self.print_trace()
            return True

        if self.make_children() == 0:
            return False

        return self.solvable_child()

There are two base cases to this `recursive function
<http://en.wikipedia.org/wiki/Recursion_(computer_science)#Recursive_functions_and_algorithms>`_.

* ``self.is_goal()`` : Goal has been reached. This Game contains a Cup that
  has 4 oz of water, success, a goal state has been found! Return ``True``
  and print a trace of how the algorithm got here.
* ``self.make_children() == 0`` : There are no child states. This Game can not
  generate any new states that don't exist in the tree already, so this state
  is a fail, return ``False``.

When neither of those two base cases are found, then this state is on a
"success path" if one of its children "is solvable". The recursive case is that
the ``Game.solvable_child`` helper function is then used to call
``Game.is_solvable`` on each of the child Games.

Here is the helper function without comments:

.. code-block:: python

    def solvable_child(self):
        for child in self.children:
            if child.is_solvable():
                return True

        return False

There are two "interesting" features of this function:

* It operates like a `short circuited OR
  <http://en.wikipedia.org/wiki/Short-circuit_evaluation>`_ reduction. This
  means that as soon as a solvable child is found, it stops searching and
  returns ``True``.
* It has been split out from ``Game.is_solvable`` to assist with unit testing.

This short circuiting feature is important. I wasn't able to get it to work in
a ``reduce`` statement on the ``Game.children``, so instead I wrote it out
explicitly as a for-loop.

Duplicate search
----------------

When generating new Games by pouring water from Cup to Cup, only new Game
states are added as children of any particular Game. This prevents duplication
of Games and ensures that the search will terminate once all different possible
states have been generated at the very latest.

The ``Game.has_game`` function implements this duplicate search using a
recursive depth first tree search.

As much functional style as possible
------------------------------------

Originally I intended to write this sketch with as much `functional style code
<http://en.wikipedia.org/wiki/Functional_programming>`_ as possible. However,
there were certainly some functions that we not possible to achieve this
without some serious hacking, and so I chose to keep those functions as simple
and testable as possible.

I'd love to have the time to come back and construct a similar sketch for this
problem in Haskell.

Possible improvements and follow up ideas
=========================================

Apart from a fully functional rewrite, there are a couple of ways that I could
see to improve the sketch. Even though it doesn't run slowly, there are
certainly some optimisations that could be made, plus some follow up ideas.

Save time by checking Cups contents when pouring
------------------------------------------------

When generating child Game states by pouring from one cup to another, the
system does not care if a Cup has water to give or if the recipient is full. It
does the pour and then eliminates the new state because it's a duplicate of its
parent.

Instead, time could be saved by improving the pouring function so that pours
only generate new Game states when there is water to give and the destination
cup has space for that water.

Improve the network anti-duplication search
-------------------------------------------

Searching the existing Game states to ensure that the same state hasn't already
been created first runs to the top of the Game tree, then searches downwards.

Most Game states will be duplicates of a Game that's either their parent or one
Game state away from them. This means there's an advantage, especially when
running bigger problem searches, to search nearest Games first.

Create a ``goal`` variable
--------------------------

The code could be improved to accept a ``goal`` value for the amount of water
that should be in a Cup for success to be achieved.

Search for bigger solvable problems
-----------------------------------

Going meta, it would be interesting now to use this code to search for a nice
big complicated water pouring problem. What's the largest number of Cups and
steps to success that can be found?

Related stuff
=============

I've always been fascinated by the power of graph searching as a replacement
for intelligence. In this example, the code has searched all possible Game
states for one that meets the success criteria.

My first introduction to this idea was via `Donald Michie
<http://www.theguardian.com/science/2007/jul/10/uk.obituaries1>`_'s  MENACE
machine. This was a noughts-and-crosses playing machine made from matchboxes.
It used a very simple algorithm, which is effectively a weighted graph, to
"learn" to play the game. `Uppsala University has an interesting project
outline for building a code version
<http://www.it.uu.se/edu/course/homepage/ai/menace>`_.

Grab me on `Twitter <https://twitter.com/jamesfublo/>`_ to share any thoughts.

Thanks for reading.
