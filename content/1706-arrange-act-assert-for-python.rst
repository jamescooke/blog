Arrange Act Assert pattern for Python developers
================================================

:date: 2017-06-27 22:00
:tags: language:python, topic:testing
:category: Code
:summary: A short guide to using the Arrange Act Assert pattern of testing with
          Python.
:scm_path: content/1706-arrange-act-assert-for-python.rst


In this post, I present a guide on how to use the Arrange Act Assert pattern in
Python unit tests. It focuses on a recognisable and reusable Python test
template which I've developed over the last couple of years, both on my own
projects and within teams.


What is Arrange Act Assert?
---------------------------

The "Arrange-Act-Assert" pattern of testing was observed and named by Bill Wake
in 2001. I first came across it in Kent Beck's book "Test Driven Development:
By Example".

The pattern helps by focusing each test on a single Action and clearly
organising the arrangement of the System Under Test (SUT) and the assertions
that are made on it after the Action.

In this way, the pattern helps by unifying the structure of tests in a suite
and improving the understanding of those working on the tests.


.. code-block:: python

    def test()
        """
        One line statement about SUT's behaviour
        """
        arrangement()

        result = action()

        assert result is valid()



Resources
---------

* http://xp123.com/articles/3a-arrange-act-assert/
