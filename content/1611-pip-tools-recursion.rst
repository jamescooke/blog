Using pip-tools and multiple requirements files
===============================================

Use a Makefile
--------------

See https://github.com/jamescooke/prlint/blob/master/requirements/Makefile

Put this in your requirements folder. It does some helpful things:

* Creates a recipe called ``all`` that will build all requirements files where
  the ``.in`` version is older than the ``.txt``. This is helpful because
  ``make`` then knows that if an ``in`` file has been updated that the
  corresponding ``txt`` file should be updated. If you want to update
  requirements do ``touch file.in`` so that the timestamp on the ``in`` file is
  updated.

* Tells ``make`` how to compile any ``txt`` file. This means you can ask for a
  single requirement file to be recompiled with ``make [filename].in``.

* Creates a dependency chain. In this file the line::

      test.txt: base.txt

  ... tells make that if ``base.txt`` is updated, then ``test.txt`` should be
  updated too.

Now you can build all requirements with:

.. code-block:: bash

    cd requirements
    make

Recursion using ``txt`` files, not ``in`` files
===============================================

    When one requirements file depends on another, should I do ``-r base.in``
    or ``-r base.txt``?

There is a versioning issue with how ``pip-tools`` works. It's a result of the
extra layer of abstraction between a list of a required libraries (kept in the
``in`` file) and a list of compiled versions and dependencies (stored in the
``txt`` file).

As a result of this, it's important to use recursive requirements through
``in`` files to point at compiled ``txt`` files rather than other ``in`` files.
For example, given the following requirements files:

* ``base.in``

  - ``test.in``

When adding ``-r base.txt`` to the top of ``test.in`` it means that
requirements set by compiling ``base.txt`` will be observed by compiling
``test.txt``. It means that requirements specified in the test file will have
to match the requirements in your base - which is what you want for testing.
