A successful `pip-tools` workflow
=================================

:date: 2016-11-11 20:00
:tags: language:python
:category: Code
:summary: Using pip-tools with multiple requirements files can be difficult.
    This post describes my current workflow that manages the complexity with a
    ``Makefile``.
:scm_path: content/1611-pip-tools-recursion.rst

In this post I present the ``pip-tools`` workflow I've been using over a number
of projects to manage multiple inherited requirements files. It uses a `GNU
Make <https://www.gnu.org/software/make/manual/make.html>`_ Makefile to provide
recipes for managing requirements and specifying the dependencies between the
requirements files.

Keep requirements files in their own folder
-------------------------------------------

In order to preserve sanity, I keep my project requirements in their own folder
directly inside the project.

.. code-block:: bash

    $ cd project
    $ ls requirements/
    base.in  base.txt  Makefile  test.in  test.txt


Store ``in`` and ``txt`` files in version control
-------------------------------------------------

``pip-tools``'s ``pip-compile`` command compiles an ``in`` file consisting of
top level requirements. It consults the PyPI index, looking up the package
versions available, outputting a specific list of pinned packages in a ``txt``
file.

Both ``in`` and ``txt`` files are tracked in the project's revision control
system (``git``). This allows for shipping of the compiled ``txt`` files for
installation, but more importantly, it presents the opportunity to check the
diff of ``txt`` files when upgrading packages.

Set ``in`` files to depend on ``txt`` files
-------------------------------------------

Given a project with two requirements files:

* ``base.in`` compiles to ``base.txt``::

* ``test.in`` compiles to ``test.txt``::

``base.in`` contains::

      project-packages

``test.in`` contains::

      -r base.txt

      test-packages

Setting ``test.in`` to depend on ``base.txt`` rather than ``base.in`` means
that the top level requirements for testing and do not override the packages
needed by the main project.

Use a Makefile for common tasks
-------------------------------

On each project that has multiple requirements files, I use `this Makefile 
<https://github.com/jamescooke/prlint/blob/master/requirements/Makefile>`_ and
place it in the requirements folder.


.. code-block::

    .PHONY: all check clean

    objects = $(wildcard *.in)
    outputs := $(objects:.in=.txt)
    PIP_TOOLS_INSTALLED: ; @which pip-compile > /dev/null

    all: $(outputs)

    %.txt: %.in
        pip-compile -v --output-file $@ $<

    test.txt: base.txt

    check: PIP_TOOLS_INSTALLED

    clean: check
        - rm *.txt

Let's go over this line by line.

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

    $ cd requirements
    $ make

TODO find out what the default recipe is

If you want to roll forwards all your dependencies you can do make clean all
and it'll make sure that you've got pip-tools installed, then remove all the
txt files, then rebuild them in the order you've told it

If in doubt about what ``make`` is about to run at any stage, it can be helpful
to ask for a dry-run and inspect the commands that were planned::

    make -n requirements

Add a dependency
----------------

To add a dependency, locate the appropriate ``*.in`` file and add just the name
of it there. The version number is only required if a particular version of the
library is required. The latest version will be chosen by default when
compiling.

In order to update a single package version, remove its lines from the compiled
corresponding ``.txt`` files. The next call to ``make requirements`` will
reevaluate the latest version for packages that do not have corresponding lines
in the ``.txt`` file and they will be updated as required.

If ``base.in`` is updated, then ``make`` knows that it will need to recompile
``base.txt`` in order to make ``test.txt``. We can see that here:

.. code-block:: bash

    $ touch base.in       # update timestamp on base.in
    $ make -n test.txt  # ask make what commands it will run for the test.txt recipe
    pip-compile -v --output-file base.txt base.in
    pip-compile -v --output-file test.txt test.in

Update all requirements
-----------------------

To update all requirements to the latest version (including updating all
packages that are not pinned in the ``.in`` file with a particular version
number), the ``clean`` recipe will clean out all ``*.txt`` files if you have
``pip-tools`` installed. Then the ``all`` recipe can be used to rebuild them
all

Finally
-------

Happy requirements packing!
