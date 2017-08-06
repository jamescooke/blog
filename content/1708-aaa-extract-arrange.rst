AAA Part 2: Extract Arrange code to make fixtures
=================================================

:date: 2017-08-04 00:00
:tags: language:python, topic:testing
:category: Code
:summary: This post explores how to extract arrangement code when working with
          the Arrange Act Assert pattern so that it can be used with certainty
          across the test suite.
:scm_path: content/1708-aaa-extract-arrange.rst

* This post is Part 2 of a series on the Arrange Act Assert pattern for Python
  developers.

* `Part 1: Arrange Act Assert pattern for Python developers is here
  </arrange-act-assert-pattern-for-python-developers.html#the-final-test>`_.


.. image:: |filename|/images/test_shape.png
    :alt: The shape of a test in Python built with Arrange Act Assert.

The test suite, like the software it's testing, is a living, dynamic and
growing code base. As it grows, like the software it's testing, there will be
duplication. In this post, I will explore duplication in the Arrange block and
show how one way to use extraction to reduce that duplication.


Sources of Duplication
----------------------

When writing tests in the AAA pattern duplication can occur in all of the
three sections:

Arrange
.......

Duplication in this section happens when tests share common setup code - this
post deals with this situation.

There are two routes I've found that result in duplication in different Arrange
blocks. I've given them my own names: "Complicated setup" and "Test
duplication" - if you know a more common name for these scenarios, then please
share.

* Complicated setup happens as a test suite grows and the complexity of the
  tests "on the outside" of the code increases. Tests will often need to
  combine a number of objects in increasingly complex states to build the SUT.

Act
...

Duplication of actions between tests is expected when using the AAA pattern
across a test suite.

For example, when testing list sorting (`as per part 1
</arrange-act-assert-pattern-for-python-developers.html#the-final-test>`_),
then there would be a number of tests all in the form ``result = lll.sort()``.
Each test would be addressing a particular case - empty list, list of similar
items, etc - and asserting that the outcomes are as expected.

Assert
......

When multiple tests need to make the same or similar assertions, then assert
code can become duplicated between tests. Extracting those common assertions
into an assertion helper can be beneficial, and I'll write about this in a
follow up post.

Let's move on and explore duplication in Arrange and solve it with Extract
Method.

Extraction as a solution
------------------------

Extract Method [#em]_ is just a tool for handling duplicated code between
tests. `Kent Beck's book "Test Driven Development: By Example"
<http://www.goodreads.com/book/show/387190.Test_Driven_Development>`_ really
turned me on to the value in eliminating duplicated code between the test and
the SUT [#sut]_.

* I'm using `pytest <https://docs.pytest.org/en/latest/>`_ in this example
  which means that fixtures are marked with the ``@pytest.fixture`` decorator.
  If you're using ``unittest`` then you could extract the set up code into the
  ``TestCase.setUp`` method.

* If you can, perform Extract Method while your test suite is GREEN [#green]_.
  This means that you can be more assured that your refactoring has worked
  without errors.

Complicated setup
-----------------

During my work, I very often build permission systems that manage access to
resources such as files, accounts, projects, etc, based on the connection
between Users and those resources. Using an example from a project is the test
below - it sets up a project on an Account: TODO

You can see that the setup is long and complicated and before we take any
actions on the SUT, there is some benefit in asserting that we've built
everything correctly. Did Homer get access? Can Marge perform additions to the
Account?

Test of the setup of the SUT will often be informed by the tests that are about
to be carried out on it. If we're about to assert that Homer can be granted
permissions, then it makes sense to assert that he did not have those
permissions already when the SUT was constructed.

But adding these assertions before the Act section means breaking AAA - this is
a smell the test has grown too complex and should be cut down.

I've used a simplified example to illustrate how to solve this below. I've
imagined a ``SUT`` class that must be called with some arrangement functions
like ``arrange_a``, ``arrange_b``, etc.

.. raw:: html

    <script async class="speakerdeck-embed" data-id="da526efe5fb6445eadb71b7f4b66c2f5" data-ratio="1.82857142857143" src="//speakerdeck.com/assets/embed.js"></script>


If the example does not load for you, you can `view it on speakerdeck
<https://speakerdeck.com/jamescooke/extract-arrangement-code>`_.

Test duplication
----------------





After this process we are back at a pair of tests with a single fixture that
fit the AAA pattern that I advocated in Part 1 of this series:

* We can continue to develop the SUT using TDD [#tdd]_ by adding new
  requirements to ``test_fixture()`` and then expanding the fixture to get back
  to GREEN.

* We are also left in a situation where we have a fixture that can be reused
  really easily. We can test the permutations of different actions on a
  particular SUT without having to depend on our power of copy and paste.

Benefits of Extraction
----------------------

Some people I've worked with have suggested that Extract Method [#em]_ should
not be used on tests because it can introduce errors and make the suite harder
to debug.

In some ways this is true. I can imagine that in our example TODO in the
future changes and this would lead to a large number of failures. However,
**without** extracting the fixture the failure would effect the ``n`` tests
that used the code - all would have to be fixed by hand. **With** extraction
there would be ``n + 1`` failures - the original failures on the code that used
the fixture, plus the additional failure from the test on the fixture itself.
However, the payoff for that additional failure is that there is the
opportunity to fix the problem in one place - the extracted code in the
fixture.

On top of that, the fix can be performed in a TDD way because the fixture is
already extracted and under test - a potential double win.

In this way the test suite remains dynamic, clear and able to adapt with the
software it's testing.

Should all fixtures have their own tests?
-----------------------------------------

I'm often asked whether I think test fixtures should be tested. My answer is:
"It depends".

When the fixture was arrived at via "Complicated setup" then my answer is
"yes". As we've seen, the ``test_fixture()`` test remains to pin the fixture's
behaviour and assert that the SUT is in the expected state.

When the fixture has been extracted because of "Test duplication" there will be
a fixture created that does not have its own explicit test. Instead the fixture
is tested implicitly by the two tests but does not have a dedicated test of its
own.

For me this is an "OK" situation and if it turns out that the fixture should be
adjusted then a fixture test can be created to facilitate that change under the
usual RED, GREEN, REFACTOR cycle.

Next in this series
-------------------

Next I will write about extraction in the Assertion section to create assertion
helpers.


Don't miss out: `subscribe and receive an email when I post the next part of
this series <http://eepurl.com/cVkaTj>`_.


Tiny glossary
-------------

.. [#sut] `System Under Test
    <https://en.wikipedia.org/wiki/System_under_test>`_ I've used this to mean the
    Unit under test, there is no implication around the size of the "system" or
    "unit".

.. [#em] Extract Method is a refactoring step `defined here
    <https://refactoring.com/catalog/extractMethod.html>`_.

.. [#tdd] Test Driven Development.

.. [#green] GREEN is the name for the state when all tests in your suite pass.
