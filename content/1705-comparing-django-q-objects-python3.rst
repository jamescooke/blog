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

In a `previous post <1603-comparing-django-q-objects.rst>`_ I wrote about
comparing Django's Q object instances. The original code was Python 2 with
unittest and was `due for an update
<https://github.com/jamescooke/blog/issues/6>`_.

The previous issue with comparing Django's Q objects remains the same:

    Django's Q object does not implement ``__cmp__`` and neither does
    ``Node`` which it extends (``Node`` is in the ``django.utils.tree`` module).

    Unfortunately, that means that comparison of Q objects that are equal fails.


A Python 3 simple solution
--------------------------

The following is a Python 3 assertion helper for use with pytest that uses the
original strategy of comparing the string versions of the Q objects.

.. code-block:: python

    from django.db.models import Q


    def assert_q_equal(left, right):
        """
        Simply test two Q objects for equality. Does is not match commutative.

        Args:
            left (Q)
            right (Q)

        Raises:
            AssertionError: When -
                * `left` or `right` are not an instance of `Q`
                * `left` and `right` are not considered equal.
        """
        assert type(left) is Q
        assert type(right) is Q
        if str(left) != str(right):
            raise AssertionError('Q{} != Q{}'.format(left, right))

This time the helper is just a function rather than a mixin for
``unittest.TestCase``.

I've made the choice of raising a custom ``AssertionError`` in the case that
the left and right sides do not match. This means that the output when two Q
objects do not match looks like::

    ____________________________ test_neq_simple ______________________________
    test_assert_q_equal.py:61: in test_neq_simple
        assert_q_equal(q_a, q_b)
    test_assert_q_equal.py:22: in assert_q_equal
        raise AssertionError('Q{} != Q{}'.format(left, right))
    E   AssertionError: Q(AND: ('location', '北京市')) != Q(AND: ('location', '北京'))

This is a nice simple output which reflects what is being compared and is
suitable for my usual testing purposes.

Alternatively, if we use ``assert`` and do not raise an ``AssertionError``,
then the comparison would be:

.. code-block:: python

    assert str(left) == str(right)

And this gives failure output that shows the string comparison::

    ______________________ test_neq_multi_not_commutative ______________________
    test_assert_q_equal.py:83: in test_neq_multi_not_commutative
        assert_q_equal(q_a, q_b)
    test_assert_q_equal.py:21: in assert_q_equal
        assert str(left) == str(right)
    E   assert "(AND: ('spee...n', 'north'))" == "(AND: ('direc...'speed', 12))"
    E     - (AND: ('speed', 12), ('direction', 'north'))
    E     + (AND: ('direction', 'north'), ('speed', 12))

Although there might be some situations where this string comparison output is
more helpful, I've gone for the custom Q object representation in my own
projects. The important thing is to adjust your assertion helpers to best fit
the needs of your test suite and team.

Final testing related note
--------------------------

Tests for ``assert_q_equal`` and its original code are `in this gist
<https://gist.github.com/jamescooke/1bed3414fee7d5c72540e567bcd63887>`_.

Happy testing!
