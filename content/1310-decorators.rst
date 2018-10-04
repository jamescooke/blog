Things to remember about decorators
###################################

:date: 2013-10-22 20:00
:tags: language:python
:category: Code
:summary: Notes to myself about Python decorators with a focus on making them testable.
:scm_path: content/1310-decorators.rst

After an interview question about Python decorators which I stumbled over, I
promised myself that I would improve my knowledge of this metaprogramming
technique.

These are my notes to myself on decorators - maybe they'll be helpful to
someone else who's improving their knowledge of decorators too.

* A decorator is pure Pythonic syntatic sugar.

* A decorator is a Python callable that receives the decorated function and
  returns a new function in its place.

  For example, if there is a decorator called `my_decorator` and we want to
  decorate `my_func` then...

  .. code-block:: python

    @my_decorator
    def my_func():
        """some stuff"""
        ...
        return

  Is equivalent to writing.

  .. code-block:: python

    def my_func():
        """some stuff"""
        ...
        return
    my_func = my_decorator(my_func)


* The decorator callable is executed at load time, not at execution time. Here
  is an example of a silly decorator that prints "Hello World" when the Python
  file is loaded - there is nothing else in the file.

  `hello.py`

  .. code-block:: python

    def say_hello(func):
        print 'Hello World'
        return func

    @say_hello
    def nothing():
        # Do nothing just return
        return

  Run it on the command line, and "Hello World" appears when the `nothing`
  function is decorated.

  .. code-block:: bash

    $ python hello.py
    Hello World


* When writing a decorator, remember to patch over the docstring of the wrapped
  function. This can be done by accessing the passed function's `__doc__`
  attribute. Failing to do so will prevent doctest from testing the decorated
  function.

  .. code-block:: python

    def my_decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        # Pass through the doc string
        wrapper.__doc__ = func.__doc__
        return wrapper

  **Update** This is actually far better done with the `wraps` decorator from
  the `functools` modules, which fixes the `__name__` and `__doc__` attributes
  to what we'd expect them to be.

  .. code-block:: python

    from functools import wraps

    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

  Found on `Improve your Python <https://jeffknupp.com/blog/2013/11/29/improve-your-python-decorators-explained/>`_.


* When unit testing decorators, one strategy can be to manually call the
  decorator on a mocked object and inspect how it interacts with it.

  Here's a caching function which is used to speed up the Fibonacci series.

  .. code-block:: python

    def cache(func):
        # Keep a dict of values returned already
        vals = {}

        def wrapper(x):
            if not vals.has_key(x):
                vals[x] = func(x)
            return vals[x]

        wrapper.__doc__ = func.__doc__

        return wrapper


  Now use the cache function as a decorator.

  .. code-block:: python

    @cache
    def fib(x):
        """Fibonacci series

        >>> fib(1)
        1
        >>> fib(2)
        2

        """
        if x < 0:
            raise ValueError('Must be greater than 0')
        elif x == 0:
            return 1
        elif x == 1:
            return 1
        else:
            return fib(x - 1) + fib(x - 2)

  And here's a unittest that asserts that the cache function only allows calls
  through when there is no value saved in the `vals` dict.

  .. code-block:: python

    import unittest
    from mock import Mock

    class TestCashDecorator(unittest.TestCase):

        def test_cache(self):
            my_fn = Mock(name='my_fn')
            my_fn.return_value = 'hi'

            wrapped = cache(my_fn)
            # First call gives a call count of 1
            self.assertEqual(wrapped(3), 'hi')
            self.assertEqual(my_fn.call_count, 1)

            # Second call keeps the call count at 1 - the cached value is used
            self.assertEqual(wrapped(3), 'hi')
            self.assertEqual(my_fn.call_count, 1)

            # Subsequent call with a new value increased the call count
            self.assertEqual(wrapped(7), 'hi')
            self.assertEqual(my_fn.call_count, 2)


* Make sure the scope of variables used in the decorators is correct, this is
  `an interesting article by Simeon Franklin about decorators and scope
  <http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/>`_.

  If in doubt, extend any tests to test a second decorated function and ensure
  that the two functions do not effect each other.

  Below is a test that aims to check that cache dictionaries are not shared
  between instances of the `cache` decorator, it is appended to the
  `test_cache` test above.

  .. code-block:: python

        # Check that the vals dict isn't shared between other decor
        my_other_fn = Mock(name='other fn')
        my_other_fn.return_value = 'other hi'
        # Create other wrapped function
        other_wrapped = cache(my_other_fn)
        self.assertEqual(other_wrapped(7), 'other hi')
        self.assertEqual(my_other_fn.call_count, 1)
        # The original function has not have been additionally called, its
        # call count remains 2
        self.assertEqual(my_fn.call_count, 2)

All suggested tips on decorators very welcome - thanks for reading!
