Comparing Django Q Objects
==========================

:data: 2016-03-26 12:00
:tags: django
:category: Code
:summary: A super simple assertion helper for comparing instances of
          Django's Q objects.

Background
----------

When building complex queries in Django ORM programmatically, it's helpful
to be able to test the resulting Q object instances against each other.

However, Django's Q object does not implement ``__cmp__`` and neither does
``Node`` which it extends (``Node`` is in the ``django.utils.tree`` module).

Therefore this fails::

    >>> from django.db.models import Q
    >>> a = Q(thing='value')
    >>> b = Q(thing='value')
    >>> assert a == b
    Traceback
    ...
    Assertion Error

This is a shame, because it makes asserting that the particular function has
produced the correct Q object in a unittest challenging.

The perfect world
-----------------

Since Q objects represent the logic of SQL ``WHERE`` clauses they are therefore
Python representations of predicates. In an ideal world the predicate logic
rules of equality could be used to compare Q objects.

Commutative would work

A && B === B && A

Double negation would work

!!A == A

Negation on expression would work

!(A && B) == !A || !B


What Django gives us
--------------------

However, in a module that doesn't even implement ``__cmp__`` this is a little out of reach.

This means that A != A, which is very sad.

Give up logical equivalence and just use structural equivalence.

Q is made from ``tree``, each Node is a ``tuple`` of field and value. Could walk this tree and compare all nodes.

However error output might not be helpful and we'd have to help the user understand what's different.


Therefore go simple
-------------------

Just compare stringy versions of objects

Advantage is simplified string comparison, which can provide rich diffs:

AssertionError: u"(AND: ('place__context', 'Residential'))" != u"(AND: ('place__context', 'Palace'))"
- (AND: ('place__context', 'Residential'))
?                           ^^^^^^^^^
+ (AND: ('place__context', 'Palace'))
?                           ^  +++

Register Q object with assertEqual in TestCase? Just be able to use assertEqual?
