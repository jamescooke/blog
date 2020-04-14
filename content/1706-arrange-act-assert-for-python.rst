Arrange Act Assert pattern for Python developers
================================================

:date: 2017-07-06 23:00
:tags: language:python, topic:testing
:category: Code
:summary: This post introduces the Arrange Act Assert pattern of testing and
          shows how it can be used in a Python context with Pytest.
:scm_path: content/1706-arrange-act-assert-for-python.rst

This is the first of two posts exploring the Arrange Act Assert pattern and
how to apply it to Python tests.
It presents a recognisable and reusable test template
following the Arrange Act Assert pattern of testing. In addition, I aim to
present strategies for test writing and refactoring which I've developed over
the last couple of years, both on my own projects and within teams.

In this first part I will introduce the Arrange Act Assert pattern and discuss its
constituent parts.


What is Arrange Act Assert?
---------------------------

The "Arrange-Act-Assert" (also AAA and 3A) pattern of testing was `observed and
named by Bill Wake in 2011
<https://xp123.com/articles/3a-arrange-act-assert/>`_. I first came across it in
`Kent Beck's book "Test Driven Development: By Example"
<https://www.goodreads.com/book/show/387190.Test_Driven_Development>`_ and I
spoke about it at `PyConUK 2016 <{filename}/1609-aaa-pyconuk.rst>`_.

The pattern focuses each test on a single action. The advantage of this focus
is that it clearly separates the arrangement of the System Under Test (SUT) and
the assertions that are made on it after the action.

On multiple projects I've worked on I've experienced organised and "clean" code
in the main codebase, but disorganisation and inconsistency in the
test suite. However when AAA is applied, I've found it helps by unifying and
clarifying the structure of tests which helps make the test suite much more
understandable and manageable.


TL;DR: The shape of an AAA test
-------------------------------

Here is a test that I was working on recently that follows the AAA pattern.
I've extracted it from Vim and blocked out the code with the colour that Vim
assigns.

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

While working on test suites that employ this pattern, my experience has been
that I've found it easier to understand each test. My eye has definitely got
used to the test "shape". Want to know what is being tested? Just look at the
clear line above the assertion block.

Follow this pattern across your tests and your suite will be much improved.


Background
----------

I'll now go into detail on each of these parts using Pytest and a toy
test example - a simple happy-path test for Python's builtin
``list.reverse`` function.

I've made the following assumptions:

* We all love `PEP008 <https://www.python.org/dev/peps/pep-0008/>`_, so we want
  tests to pass ``flake8`` linting.

* `PEP020, The Zen of Python <https://www.python.org/dev/peps/pep-0020/>`_, is
  also something we work towards - I will use some of it's "mantras" when I
  justify some of the suggestions in this guide.

* Simplicity trumps performance. We want a test suite that is easy to maintain
  and manage and can pay for that with some performance loss. I've assumed this
  is a reasonable trade off because the tests are run much less frequently than
  the SUT in production.

This post is only an introduction to the AAA pattern. Where certain topics will
be covered in more detail in future posts in this series, I have marked them
with a footnote.


Definition
----------

The definition of the test function.

Example
.......

.. code-block:: python

    def test_reverse():

Guidelines
..........

* Name your function something descriptive because the function name will be
  shown when the test fails in Pytest output.

* Good test method names can make docstrings redundant in simple tests (`thanks
  Adam! <https://github.com/jamescooke/blog/pull/10#discussion_r125855056>`_).


Docstring
---------

An optional short single line statement about the behaviour under test.

Example
.......

.. code-block:: python

    """
    list.reverse inverts the order of items in a list, in place
    """

Guidelines
..........

Docstrings are not part of the AAA pattern. Consider if your test needs one or
if you are best to omit it for simplicity.

If you do include a docstring, then I recommend that you:

* Follow the existing Docstring style of your project so that the tests are
  consistent with the code base you are testing.

* Keep the language positive - state clearly what the expected behaviour is.
  Positive docstrings read similar to:

      X does Y when Z

  Or...

      Given Z, then X does Y

* Be cautious when using any uncertain language in the docstring and follow the
  mantra "Explicit is better than implicit" (`PEP20
  <https://www.python.org/dev/peps/pep-0020/>`_)

  Words like "should" and "if" introduce uncertainty. For example:

      X should do Y if Z

  In this case the reader could be left with questions. Is X doing it right at
  the moment? Is this a ``TODO`` note? Is this a test for an expected failure?

  In a similar vein, avoid future case.

      X will do Y when Z

  Again, this reads like a ``TODO``.


Arrange
-------

The block of code that sets up the conditions for the test action.

Example
.......

There's not much work to do in this example to build a list, so the arrangement
block is just one line.

.. code-block:: python

    greek = ['alpha', 'beta', 'gamma', 'delta']


Guidelines
..........

* Use a single block of code with no empty lines.

* Do not use ``assert`` in the Arrange block. If you need to make an assertion
  about your arrangement, then this is a smell that your arrangement is too
  complicated and should be extracted to a fixture or setup function and tested
  in its own right.

* Only prepare non-deterministic results not available after action.

* The arrange section should not require comments. If you have a large
  arrangement in your tests which is complex enough to require detailed
  comments then consider:

  - Extracting the comments into a multi-line docstring.

  - Extracting the arrangement code into a fixture and testing that the fixture
    is establishing the expected conditions as previously mentioned.


Act
---

The line of code where the Action is taken on the SUT.

Example
.......

.. code-block:: python

        result = greek.reverse()

Guidelines
..........

* Start every Action line with ``result =``.

  This makes it easier to distinguish test actions and means you can avoid the
  hardest job in programming: naming. When every result is called ``result``,
  then you do not need to waste brain power wondering if it should be ``item =``
  or ``response =`` etc. An added benefit is that you can find test actions
  easily with a tool like ``grep``.

* Even when there is no result from the action, capture it with ``result =``
  and then ``assert result is None``. In this way, the SUT's behaviour is
  pinned.

* If you struggle to write a single line action, then consider extracting some
  of that code into your arrangement.

* The action can be wrapped in ``with ... raises`` for expected exceptions. In
  this case your action will be two lines surrounded by empty lines.


Assert
------

The block of code that performs the assertions on the state of the SUT after
the action.

Example
.......

.. code-block:: python

        assert result is None
        assert greek == ['delta', 'gamma', 'beta', 'alpha']

Guidelines
..........

* Use a single block of code with no empty lines.

* First test ``result``, then side effects.

* Limit the actions that you make in this block. Ideally, no actions should
  happen, but that is not always possible.

* Use simple blocks of assertions. If you find that you are repeatedly writing
  the same code to extract information from the SUT and perform assertions on
  it, then consider extracting an assertion helper.


The final test
--------------

Here's the example test in full:

.. code-block:: python

    def test_reverse():
        """
        list.reverse inverts the order of items in a list, in place
        """
        greek = ['alpha', 'beta', 'gamma', 'delta']

        result = greek.reverse()

        assert result is None
        assert greek == ['delta', 'gamma', 'beta', 'alpha']


flake8-aaa
----------

Check out `flake8-aaa <https://flake8-aaa.readthedocs.io/en/stable/>`_ - a
Flake8 plugin that makes it easier to write tests that follow the Arrange Act
Assert pattern outlined above.

Thanks
------

I hope that this introduction has been helpful and you will return for part 2:
`AAA Part 2: Extracting Arrange code to make fixtures
</aaa-part-2-extracting-arrange-code-to-make-fixtures.html>`_.

Thanks to `Adam <https://adamj.eu/>`_ for reviewing this post and his helpful
feedback.

Thanks for reading and happy testing!
