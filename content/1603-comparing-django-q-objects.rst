Comparing Django Q Objects
==========================

:date: 2016-03-27 20:00
:tags: django
:category: Code
:summary: A super simple assertion helper for comparing instances of Django's Q
          objects.
:scm_path: content/1603-comparing-django-q-objects.rst

Background
----------

When programmatically building complex queries in Django ORM, it's helpful
to be able to test the resulting `Q object instances
<https://docs.djangoproject.com/en/1.8/topics/db/queries/#complex-lookups-with-q>`_
against each other.

However, Django's Q object does not implement ``__cmp__`` and neither does
``Node`` which it extends (``Node`` is in the ``django.utils.tree`` module).

Unfortunately, that means that comparison of Q objects that are equal fails.

.. code-block:: python

    >>> from django.db.models import Q
    >>> a = Q(thing='value')
    >>> b = Q(thing='value')
    >>> assert a == b
    Traceback (most recent call last)
    ...
    Assertion Error:

This means that writing unittests that assert that correct Q objects have been
created is hard.

A simple solution
-----------------

Q objects generate great Unicode representations of themselves.

.. code-block:: python

    >>> a = Q(place='Residential') & Q(people__gt=5)
    >>> unicode(a)
    u"(AND: ('place', 'Residential'), ('people__gt', 5))"

Plus, I like to write assertion helpers whenever I have something complicated
to test frequently in a test suite.

Therefore a really simple solution is an assertion helper that would compare Q
objects by:

* Asserting that left and right sides are both instances of ``Q``.

* Asserting that the Unicode for the left and right sides are identical.

So here's a mixin that does that which can be added to any
``unittest.TestCase`` (such as Django's default ``TestCase``):

.. code-block:: python

    from django.db.models import Q


    class QTestMixin(object):

        def assertQEqual(self, left, right):
            """
            Assert `Q` objects are equal by ensuring that their
            unicode outputs are equal (crappy but good enough)
            """
            self.assertIsInstance(left, Q)
            self.assertIsInstance(right, Q)
            left_u = unicode(left)
            right_u = unicode(right)
            self.assertEqual(left_u, right_u)

Disadvantage of this method is that it is simplistic and doesn't find all the Q
objects that are identical (see below). However, the advantage is that it
provides rich diffs on failure:

.. code-block:: python

    class TestFail(TestCase, QTestMixin):

        def test_unhappy(self):
            """
            Two Q objects are not the same
            """
            a = Q(place='Residential')
            b = Q(place='Palace')
            self.assertQEqual(a, b)

Gives output:

.. code-block:: sh

    AssertionError: u"(AND: ('place', 'Residential'))" != u"(AND: ('place', 'Palace'))"
    - (AND: ('place', 'Residential'))
    ?                  ^^^^^^^^^
    + (AND: ('place', 'Palace'))
    ?                  ^  +++

Which can be very helpful when trying to track down errors.

The perfect world: Predicate Logic
----------------------------------

Since Q objects represent the logic of SQL ``WHERE`` clauses they are therefore
Python representations of predicates. In an ideal world the predicate logic
rules of equality could be used to compare Q objects and this would be built
directly into ``Q.__cmp__``.

This would mean that:

.. code-block:: python

    # WARNING MAGIC IMAGINARY CODE!

    # Commutative would work
    >>> a = Q(x=1) | Q(x=2)
    >>> b = Q(x=2) | Q(x=1)
    >>> a == b
    True

    # Double negation would work
    >>> a = Q(x=1)
    >>> b = ~~(Q=1)
    >>> a == b
    True

    # Negation on expression would work
    >>> a = ~(Q(x=1) & Q(x=2))
    >>> b = ~Q(x=1) & ~Q(x=2)
    >>> a == b
    True

This is probably never going to be implemented in Django, because it would be
functionality only used (as far as I can see) for testing. In addition, it
would start to make it hard to distinguish differences between objects when
mismatches are found.

Therefore I'd vote for the simple option most times.
