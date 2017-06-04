Comparing Django Q Objects in Python 3 with pytest
==================================================

:date: 2017-05-30 22:00
:tags: topic:testing, language:python, topic:django
:category: Code
:summary: An updated simple assertion helper for comparing instances of
    Django's Q objects using pytest in Python 3.
:scm_path: content/1705-comparing-django-q-objects-python3.rst

Background
----------

In a `previous post <{filename}/1603-comparing-django-q-objects.rst>`_ I wrote
about comparing Django's Q object instances. The original code was Python 2
with unittest and was `due for an update
<https://github.com/jamescooke/blog/issues/6>`_.

The previous issue with comparing Django's Q objects remains the same:

    Django's Q object does not implement ``__cmp__`` and neither does
    ``Node`` which it extends (``Node`` is in the ``django.utils.tree`` module).

    Unfortunately, that means that comparison of Q objects that are equal fails.


A simple Python 3 solution
--------------------------

The following is a Python 3.6 assertion helper for use with pytest that uses
the original strategy of comparing the string versions of the Q objects.

.. code-block:: python

    from django.db.models import Q


    def assert_q_equal(left, right):
        """
        Test two Q objects for equality. Does is not match commutative.

        Args:
            left (Q)
            right (Q)

        Raises:
            AssertionError: When -
                * `left` or `right` are not an instance of `Q`
                * `left` and `right` are not considered equal.
        """
        assert isinstance(left, Q), f'{left.__class__} is not subclass of Q'
        assert isinstance(right, Q), f'{right.__class__} is not subclass of Q'
        assert str(left) == str(right), f'Q{left} != Q{right}'


This time the helper is just a function rather than a mixin for
``unittest.TestCase``.

``isinstance`` is used for comparison so that any instance of a class derived
from ``Q`` can also be matched. The assertions have secondary expressions in
the form of `f-strings
<https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep498>`_ to give
helpful output without raising a custom
assertion.

When two ``Q`` instances do not match, pytest shows the following output::

    ______________________ test_neq_multi_not_commutative ______________________
    test_assert_q_equal.py:83: in test_neq_multi_not_commutative
        assert_q_equal(q_a, q_b)
    test_assert_q_equal.py:22: in assert_q_equal
        assert str(left) == str(right), f'Q{left} != Q{right}'
    E   AssertionError: Q(AND: ('speed', 12), ('direction', 'north')) != Q(AND: ('direction', 'north'), ('speed', 12))
    E   assert "(AND: ('spee...n', 'north'))" == "(AND: ('direc...'speed', 12))"
    E     - (AND: ('speed', 12), ('direction', 'north'))
    E     + (AND: ('direction', 'north'), ('speed', 12))
    ==================== 1 failed, 7 passed in 0.07 seconds ====================

The important thing is to adjust your assertion helpers to best fit
the needs of your test suite and team.

Final testing related note
--------------------------

Thanks to `Adam's feedback on my initial post
<https://github.com/jamescooke/blog/pull/7#pullrequestreview-41177014>`_, I
improved the assertions to use ``isinstance`` and secondary expressions to
provide helpful output.

Tests for ``assert_q_equal`` and its original code are `in this gist
<https://gist.github.com/jamescooke/1bed3414fee7d5c72540e567bcd63887>`_.

Happy testing!
