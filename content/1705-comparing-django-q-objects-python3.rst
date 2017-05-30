Comparing Django Q Objects in Python 3 with pytest
==================================================

:date: 2017-05-30 22:00
:tags: topic:testing, language:python, topic:django
:category: Code
:summary: An updated super simple assertion helper for comparing instances of
          Django's Q objects using pytest in Python 3.
:scm_path: content/1705-comparing-django-q-objects-python3.rst

Background
----------

In a `previous post <1603-comparing-django-q-objects.rst>`_ I wrote about
comparing Django's Q object instances. This original post's code was Python 2,
used unittest and was `due for an update
<https://github.com/jamescooke/blog/issues/6>`_.

The previous issue with comparing Django's Q objects remains the same as when I
wrote the original post:

    Django's Q object does not implement ``__cmp__`` and neither does
    ``Node`` which it extends (``Node`` is in the ``django.utils.tree`` module).

    Unfortunately, that means that comparison of Q objects that are equal fails.


A Python 3 simple solution
--------------------------

Using the same strategy of using the string version of the Q object for
comparison, I've created an updated assertion helper. (This time it's simply a
function rather than a mixin, which is far simpler.)

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


I've made the choice of raising my own ``AssertionError`` in the case that the
left and right sides do not match, the output looks like::

    ____________________________ test_neq_simple ______________________________
    test_assert_q_equal.py:61: in test_neq_simple
        assert_q_equal(q_a, q_b)
    test_assert_q_equal.py:22: in assert_q_equal
        raise AssertionError('Q{} != Q{}'.format(left, right))
    E   AssertionError: Q(AND: ('location', '北京市')) != Q(AND: ('location', '北京'))

If I had used a simple ``assert str(left) == str(right)`` then the output would
look as follows, which is far less clean because it shows the string
comparison::

    ______________________ test_neq_multi_not_commutative ______________________
    test_assert_q_equal.py:83: in test_neq_multi_not_commutative
        assert_q_equal(q_a, q_b)
    test_assert_q_equal.py:21: in assert_q_equal
        assert str(left) == str(right)
    E   assert "(AND: ('spee...n', 'north'))" == "(AND: ('direc...'speed', 12))"
    E     - (AND: ('speed', 12), ('direction', 'north'))
    E     + (AND: ('direction', 'north'), ('speed', 12))


Final testing related note
--------------------------

TODO Tests for ``assert_q_equal`` are `in this gist
  <https://gist.github.com/jamescooke/b9bd5afba3a7253d53bd>`_.
