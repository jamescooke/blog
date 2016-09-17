Cleaner unit testing with the Arrange Act Assert pattern
========================================================

:date: 2016-09-18 20:00
:tags: language:python, topic:testing
:category: Talk
:summary: TODO
:scm_path: content/1609-aaa-pyconuk.rst
:slug: pyconuk
:status: draft


Resources
---------

* `PEP08 <https://www.python.org/dev/peps/pep-0008/>`_ and `PEP20
  <https://www.python.org/dev/peps/pep-0020/>`_.

* `Kent Beck: Test Driven Development: By Example
  <http://www.goodreads.com/book/show/387190.Test_Driven_Development>`_ - a
  great book which references the AAA pattern (page 97).

* `Google-style docstrings
  <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_:
  In addition to using this style in my AAA tests, I've started to add a
  ``Trusts`` section to indicate which other tests are trusted by any
  particular test and why.

* `Bill Wake's post about AAA
  <http://xp123.com/articles/3a-arrange-act-assert/>`_: Bill Wake is cited by
  Kent Beck as having coined the term ``3A``.

* `Extract Method <http://refactoring.com/catalog/extractMethod.html>`_: I've
  used extract method as defined by Martin Fowler. See also `Extract Variable
  <http://refactoring.com/catalog/extractVariable.html>`_.

Finally
-------

Thanks again to `Carles <https://github.com/txels>`_ for introducing me to the
AAA pattern. Check out his `data driven tests library
<https://github.com/txels/ddt>`_.
