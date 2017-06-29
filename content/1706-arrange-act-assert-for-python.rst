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


The shape of a test
-------------------

Here is a test that I was working on recently. I've extracted it from Vim and
blocked out the code with the colour that Vim assigns for Python code.
Hopefully, in this rough image you will see three sections to the test:

.. image:: |filename|/images/test_shape.png
    :alt: The shape of a test in Python built with Arrange Act Assert.


* First there is the test definition, docstring and Arrangement.

* In the middle, there is a single line of code - this is the most important
  part: The Act.

* Finally there are the Assertions. You can see that the Assert block code
  lines all start with the orange / brown colour - that is because the Python
  keyword ``assert`` is marked with this colour in Vim with my current
  configuration.

I'll now go into detail on each of these parts using Pytest and a simple toy
test example. We'll write a simple happy-path test for Python's builtin
``list.reverse`` function.


Definition
----------

.. code-block:: python

    def test_reverse()

* Name your function something descriptive because the function name will be
  shown when the test fails in Pytest output.


Docstring
---------

.. code-block:: python

    """
    list.reverse inverts the order of items in a list, in place
    """

* A short single line statement about the behaviour under test.

* Keep the language positive - state clearly what the expected behaviour is.
  Positive docstrings read similar to:

      X does Y when Z

      Given Z, then X does Y

* Be careful with using uncertain language in the docstring. Words like
  "should" and "if" introduce uncertainty. For example:

      X should do Y if Z

  OK, so X should do Y... Is it doing it right at the moment? Is this a
  ``TODO`` note?

  We're aiming for simplicity and clarity in our tests, so definitely clear out
  any indefinite language.


Arrange
-------

.. code-block:: python

        arrangement()

* Do not use ``assert`` in the Arrange block. If you need to make an assertion
  about your arrangement, then this is a smell that your arrangement is too
  complicated and should be extracted to a fixture or setup function and tested
  in its own right.


Act
---

.. code-block:: python

        result = action()

* This is a single line 

Assert
------

.. code-block:: python

        assert result is valid()


Caveats
-------

Complicated tests and comments
::::::::::::::::::::::::::::::

Ideally every test should be simple and compact enough that a one line
docstring is sufficient to describe the test. However, this is not always the
case and sometimes a larger docstring is appropriate to help others understand
the test.

Extraction of common code
:::::::::::::::::::::::::


Resources
---------

* http://xp123.com/articles/3a-arrange-act-assert/
