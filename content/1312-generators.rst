Python generators and yield
###########################

:date: 2013-12-14 16:00
:tags: python
:category: Code
:summary: Notes to myself on generators and how to create them with generator
          expressions and the yield statement.
:scm_path: content/1312-generators.rst


It started with an interview
----------------------------

Last week in an interview for a Django developer job, I was asked:

.. code-block:: python

    thing = (x**2 for x in xrange(10))

..

    What is the type of thing?


Although I was able to identify that the type is dependent on the `()` around
the list-comprehension-like-construction, I didn't know the exact type that
`thing` would be.

The answer is a **generator**.

This post shows some of the functionalities of generators and how they can
be used in Python control flow.


Generator expressions
---------------------

Generators can be created with generator expressions. A generator expression is
a bit like a list comprehension. List Comprehension uses square brackets
`[]`. In Python...

.. code-block:: python

    >>> [x**2 for x in range(10)]

::

    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]


A generator expression is a shortcut that allows generators to be created
easily with a similar syntax - this time it's using parentheses `()`.

.. code-block:: python

    >>> (x**2 for x in range(10))

::

    <generator object <genexpr> at 0x2fa5eb0>


Generators are iterators
------------------------

Generators "provide a convenient way to implement the iterator protocol".

In Python, an `iterator
<http://docs.python.org/2.7/library/stdtypes.html#typeiter>`_ provides two key
functions, `__iter__` and `next`, so a generator itself must provide these two
functions:

.. code-block:: python

    >>> my_gen = (x**2 for x in range(10))
    >>> my_gen.__iter__
    <generator object <genexpr> at 0x293c3c0>

`__iter__` is there and returns the generator, now for `next`...

.. code-block:: python

    >>> my_gen.next()
    0
    >>> my_gen.next()
    1

Therefore `next` works. We can keep hitting until...

.. code-block:: python

    >>> my_gen.next()
    81
    >>> my_gen.next()
    ---------------------------------------------------------------------------
    StopIteration                             Traceback (most recent call last)
    <ipython-input-19-b28d59f370d8> in <module>()
    ----> 1 zzz.next()

    StopIteration: 

A `StopIteration` is raised - so the generator does everything we'd expect it
to by the iterator protocol.


Building a generator with yield
-------------------------------

Although it's not clear from the example above, a generator is able to
relinquish control and return a value - while saving its state. It then allows
the control to pass back to the structure that called it, until it's called
again, picking up where it left off.

This allows for loops over sets of values to be programmed, without the full
list of values being calculated first. A generator can be used so that `next`
is called before each iteration required.

In this way, only the values required for each iteration need to be computed.


The yield keyword - simple example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding `yield` to a function allows for generators to be constructed
'manually'.

At its very simplest, a function could be written just to generate a single
value. However, to show that a generator can return to its previous state when
called again, let's make one with two values. For example...

.. code-block:: python

    def two_things():
        yield 1
        yield 'hi'

Now we can make an instance of the generator.

.. code-block:: python

    >>> my_things = two_things()
    >>> my_things
    <generator object two_things at 0x31d0960>

And we can ask for next value.

.. code-block:: python

    >>> my_things.next()
    1

Now when we call `next` again, our generator continues from the state of the
last yield.

.. code-block:: python

    >>> my_things.next()
    'hi'

So you see how different values can be returned, one after the other.

And after that second thing, the generator now raises a `StopIteration`, since
it has no further values to return.

Since a generator implements the iterator protocol, it can be used in a `for`
statement and therefore in a list comprehension. This makes for a convenient
way to check the values of a limited generator like this one.

.. code-block:: python

    >>> [x for x in two_things()]
    [1, 'hi']

More complex example with yield
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So let's write Fibonacci as a generator. I'm going to start with doctests to
create the definition of the function, then put the code at the end.

What I like about the doctests in this example is that in 3 `fib` is tested
with `next`, but in 4 it's tested using a list comprehension.

.. code-block:: python

    def fib(last):
        """

        1.  Creates a generator
        >>> type(fib(0))
        <type 'generator'>

        2.  fib(0) just generates 0th value (1)
        >>> zero_fib = fib(0)
        >>> zero_fib.next()
        1
        >>> zero_fib.next()
        Traceback (most recent call last):
        ...
        StopIteration

        3.  fib(1) creates a generator that creates 0th (1) and 1st (1) values of
            fib seq
        >>> one_fib = fib(1)
        >>> one_fib.next()
        1
        >>> one_fib.next()
        1
        >>> one_fib.next()
        Traceback (most recent call last):
        ...
        StopIteration

        4.  fib(10) generates the first 10 fibonacci numbers
        >>> [x for x in fib(10)]
        [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

        """
        result = 1
        x = 0
        a = 1
        b = 0

        while x <= last:
            yield result

            result = a + b
            b = a
            a = result
            x += 1

That's all - have fun with generators!
