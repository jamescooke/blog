Arrange Act Assert pattern for Python developers
================================================

:date: 2017-06-27 22:00
:tags: language:python, topic:testing
:category: Code
:summary: A short guide to using the Arrange Act Assert pattern of testing with
          Python.
:scm_path: content/1706-arrange-act-assert-for-python.rst
:status: draft


In this post, I present a guide on how to use the Arrange Act Assert pattern in
Python unit tests. It focuses on a recognisable and reusable test template
which I've developed over the last couple of years, both on my own projects and
within teams.


What is Arrange Act Assert?
---------------------------

The "Arrange-Act-Assert" (also AAA and 3A) pattern of testing was observed and
named by Bill Wake in 2001. I first came across it in Kent Beck's book "Test
Driven Development: By Example".

The pattern helps by focusing each test on a single action. It clearly
separates the arrangement of the System Under Test (SUT) and the assertions
that are made on it after the action.

On multiple projects I've worked on I've experienced organised and "clean" code
in the main codebase, but complete disorganisation and inconsistency in the
test suite. However when applying AAA I've found it helps by unifying and
clarifying the structure of tests which helps make the test suite much more
understandable and manageable.


The shape of a test
-------------------

Here is a test that I was working on recently - I've extracted it from Vim and
blocked out the code with the colour that Vim assigns.

.. image:: |filename|/images/test_shape.png
    :alt: The shape of a test in Python built with Arrange Act Assert.

Hopefully in this rough image you will see three sections to the test separated
by an empty line:

* First there is the test definition, docstring and Arrangement.

* Empty line.

* In the middle, there is a single line of code - this is the most important
  part: The Act.

* Empty line.

* Finally there are the Assertions. You can see that the Assert block code
  lines all start with the orange / brown colour - that is because the Python
  keyword ``assert`` is marked with this colour in Vim with my current
  configuration.

Background
----------

I'll now go into detail on each of these parts using Pytest and a simple toy
test example. We'll write a simple happy-path test for Python's builtin
``list.reverse`` function. As we go through I'll assume that:

* We all want all test code that passes linking with ``flake8``. PEP008 is
  beneficial to our way of working.

* PEP020 is also something we work towards. I will use some of it's "mantras"
  when I justify some of the suggestions in this guide.

* Simplicity trumps performance. We want a test suite that is easy to maintain
  and manage and may in some cases pay for that with some performance loss.
  This is a reasonable trade off because the tests are run much less frequently
  than the SUT in production.


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

* Follow the existing Docstring style of your project so that the tests are
  consistent with the code base you are testing.

* Keep the language positive - state clearly what the expected behaviour is.
  Positive docstrings read similar to:

      X does Y when Z

  Or...

      Given Z, then X does Y

* Be careful with using uncertain language in the docstring. Words like
  "should" and "if" introduce uncertainty. For example:

      X should do Y if Z

  In this case the reader could be left with questions. Is X doing it right at
  the moment? Is this a ``TODO`` note? Is this a test for an expected failure?

  Since we have "Explicit is better than implicit" (`PEP20
  <https://www.python.org/dev/peps/pep-0020/>`_), then definitely clear out any
  indefinite language in your test docstrings.


Arrange
-------

.. code-block:: python

        arrangement()

* Single block of code.

* Do not use ``assert`` in the Arrange block. If you need to make an assertion
  about your arrangement, then this is a smell that your arrangement is too
  complicated and should be extracted to a fixture or setup function and tested
  in its own right.

* Only prepare non-deterministic results not available after action.

* Should not require comments.


Act
---

.. code-block:: python

        result = action()

* Use ``result =`` format.

* This is a single line.

* Can be wrapped in ``with ... raises`` for expected exceptions.

Assert
------

.. code-block:: python

        assert result is valid()

* Single block of code.

* No actions should happen.

* Test ``result`` first then side effects.

* Use simple blocks of assertions.


Caveats
-------

Assertions in Arrange
:::::::::::::::::::::


Complicated tests and comments
::::::::::::::::::::::::::::::

Ideally every test should be simple and compact enough that a one line
docstring is sufficient to describe the test. However, this is not always the
case and sometimes a larger docstring is appropriate to help others understand
the test.

Extraction of common code
:::::::::::::::::::::::::

Ideally, when there is duplicate code in different Arrange blocks, then this
should be extracted into a separate function or fixture. How to manage that
extraction and test the fixture will be part of a separate post.


Resources
---------

* http://xp123.com/articles/3a-arrange-act-assert/
