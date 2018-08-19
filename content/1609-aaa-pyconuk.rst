Cleaner unit testing with the Arrange Act Assert pattern
========================================================

:date: 2016-09-18 20:00
:tags: language:python, topic:testing
:category: Talk
:summary: My PyConUK 2016 talk about the AAA pattern for unit tests and how
          using it can help us all make our tests cleaner, easier to read
          and as Pythonic as possible.
:scm_path: content/1609-aaa-pyconuk.rst

At `PyConUK 2016
<https://2016.pyconuk.org/talks/cleaner-unit-testing-with-the-arrange-act-assert-pattern/>`_
I spoke about the Arrange Act Assert pattern and how it can help clean up unit
tests.

    **Note:** A newer post `Arrange Act Assert pattern for Python developers
    <{filename}/1706-arrange-act-assert-for-python.rst>`_ is available. It has
    much clearer examples and guidelines for using AAA than the video and
    slides below.


Original proposal
-----------------

PyConUK ask that we provide an explanation of why we think that attendees
will be interested in our talk. This was my original proposal's reasoning.

    This talk focuses on developers that practise TDD, or want to use it
    more in their coding.

    My assumption is that our community feels a lot of pain from testing.
    I've heard fellow developers talk about the difficulty with managing
    complicated test suites; issues with reading and understanding others'
    tests; and struggles when updating others' tests. I hope that the
    PyConUK attendees will have felt some of this pain be interested in a
    talk that demonstrates the use of a pattern that can (hopefully)
    mitigate some of it and help us all to be "cleaner" testers.

    Although I've marked "moderately experienced" I think that my talk
    would have a broad appeal: Those who are new to testing and would like
    a "template" to follow. And those who are expert because of the
    discussion about when to DRY out tests and how to assert that our test
    refactors are safe.

Slides and video
----------------

The video of the talk does not capture much of the screen, so the slides are
posted here too.

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/GGw5T1mw9vU" frameborder="0" allowfullscreen></iframe>

.. raw:: html

    <script async class="speakerdeck-embed" data-id="d25e0e15acef4ccc8fe70abba5adce03" data-ratio="1.33333333333333" src="//speakerdeck.com/assets/embed.js"></script>

Resources
---------

* `PEP08 <https://www.python.org/dev/peps/pep-0008/>`_ and `PEP20, The Zen of Python
  <https://www.python.org/dev/peps/pep-0020/>`_.

* `Kent Beck: Test Driven Development: By Example
  <https://www.goodreads.com/book/show/387190.Test_Driven_Development>`_ - a
  great book which references the AAA pattern (page 97).

* `Google-style docstrings
  <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_:
  In addition to using this style in my AAA tests, I've started to add a
  ``Trusts`` section to indicate which other tests are trusted by any
  particular test and why.

* `Bill Wake's post about AAA
  <https://xp123.com/articles/3a-arrange-act-assert/>`_: Bill Wake is cited by
  Kent Beck as having coined the term ``3A``.

* `Extract Method <https://refactoring.com/catalog/extractMethod.html>`_: I've
  used extract method as defined by Martin Fowler. See also `Extract Variable
  <https://refactoring.com/catalog/extractVariable.html>`_.

    **Update August 2018:** Check out `flake8-aaa
    <https://flake8-aaa.readthedocs.io/en/stable/>`_ - a Flake8 plugin that
    makes it easier to write tests that follow the Arrange Act Assert pattern.

Finally
-------

Thanks again to `Carles <https://github.com/txels>`_ for introducing me to the
AAA pattern.
