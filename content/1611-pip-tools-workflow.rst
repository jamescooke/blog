A successful `pip-tools` workflow for managing Python package requirements
==========================================================================

:date: 2016-11-13 23:00
:tags: language:python
:category: Code
:summary: Using pip-tools with multiple requirements files can be difficult.
    This post describes my current workflow that manages the complexity with a
    ``Makefile``.
:scm_path: content/1611-pip-tools-workflow.rst

In this post I present the ``pip-tools`` workflow I've been using over a number
of projects to manage multiple inherited requirements files. At its core is a
`GNU Make <https://www.gnu.org/software/make/manual/make.html>`_ Makefile to
provide recipes for managing requirements and specifying the dependencies
between the requirements files.

If you are not aware of the excellent ``pip-tools`` `package
<https://github.com/jazzband/pip-tools>`_ it provides two commands: 
``pip-compile`` and ``pip-sync``. In this post I will be focusing on using 
``pip-compile`` to compile ``.in`` files consisting of top level requirements.

``pip-compile`` consults the PyPI index for each top level package required,
looking up the package versions available, outputting a specific list of pinned
packages in a ``.txt`` file. This extra layer of abstraction (``.in`` files
containing top level requirements rather than just outputting ``.txt`` files
with ``pip freeze``) is very helpful for managing requirements, but does create
some complications which mean that a solid workflow is essential for stable
package management.


Keep requirements files in their own folder
-------------------------------------------

In order to preserve sanity, I keep my project requirements in their own folder
directly inside the project.

.. code-block:: sh

    $ cd project
    $ ls requirements/
    base.in  base.txt  Makefile  test.in  test.txt

During this post, I'll use this simple example with one set of "base"
requirements and one set of "test" requirements.


Store ``.in`` and ``.txt`` files in version control
---------------------------------------------------

Both ``.in`` and ``.txt`` files are tracked in the project's revision control
system, for example ``git``. This allows for shipping of the compiled ``.txt``
files for installation, but more importantly, it presents the opportunity to
check the diff of ``.txt`` files when upgrading packages.

I also tend to keep ``.in`` files sorted alphabetically.


Set ``.in`` files to depend on ``.txt`` files
---------------------------------------------

In the example project there are ``base.in`` and ``test.in`` requirements
files:

* ``base.in`` compiles to ``base.txt``

* ``test.in`` compiles to ``test.txt``

I want the test requirements added to the base requirements **without changing
the versions** of the packages compiled for base. Therefore I set ``test.in``
to ``-r`` require the ``base.txt`` compiled requirements:

``base.in`` contains::

      project-packages

``test.in`` contains::

      -r base.txt

      test-packages

Setting ``test.in`` to depend on ``base.txt`` rather than ``base.in`` means
that the top level requirements for testing do not override the packages
needed by the main project.


Use a Makefile for common tasks
-------------------------------

On each project that has multiple requirements files, I use a Makefile and
place it in the requirements folder.

.. code-block:: make

    .PHONY: all check clean

    objects = $(wildcard *.in)
    outputs := $(objects:.in=.txt)

    all: $(outputs)

    %.txt: %.in
        pip-compile -v --output-file $@ $<

    test.txt: base.txt

    check:
        @which pip-compile > /dev/null

    clean: check
        - rm *.txt

.. **

Here is that same file `in a current project
<https://github.com/jamescooke/prlint/blob/master/requirements/Makefile>`_.
**NOTE** that because ``make`` requires recipes to be indented by tabs, if you
want to copy this file then it could be helpful to pull the `raw file from
Github
<https://raw.githubusercontent.com/jamescooke/prlint/master/requirements/Makefile>`_
rather than copying and pasting out of this webpage where the tabs have not
been reproduced.

Let's go over the key functionality provided by this Makefile:

* First two definitions:

  .. code-block:: make

      objects = $(wildcard *.in)

  .. **

  ``objects`` is a list containing every ``.in`` file in requirements folder.

  .. code-block:: make

      outputs := $(objects:.in=.txt)

  ``outputs`` is also a list made of one ``.txt`` filename for each ``.in`` file
  in the ``outputs`` list. The ``.txt`` files do not need to exist yet, this
  list tells ``make`` what they should be called. 

* A recipe called ``all`` to build all ``.txt`` files:

  .. code-block:: make

      all: $(outputs)

  The ``all`` recipe has no commands of its own - it solely depends on all the
  ``.txt`` files in the ``outputs`` list being built. In order to fulfil this
  recipe, ``make`` will attempt to build  every ``.txt`` file in the ``objects``
  list.

* Up until now, ``make`` does not know how to build a ``.txt`` file, so here we
  give it a recipe:

  .. code-block:: make

      %.txt: %.in
          pip-compile -v --output-file $@ $<

  The first line tells ``make`` that any ``.txt`` file depends on the ``.in``
  file with the same name. ``make`` will check the date stamp on the two files
  and compare them - if the ``.txt`` file is older than the ``.in`` file or does
  not exist, then ``make`` will build it.

  The next line tells ``make`` the command to use to perform the build - it is
  the ``pip-compile`` command with the following flags:

  - ``-v`` means ``pip-compile`` will give verbose output. I find this helpful
    for general watchfulness, but you may prefer to remove it.
  
  - ``output-file $@`` means "send the output to the target of the recipe", which
    is the ``.txt`` file we've asked to be made. For example when invoking ``make
    base.txt``, then ``--output-file base.txt`` will be passed.
  
  - ``$<`` at the end is the corresponding ``.in`` input file. Make matches the
    names using the ``%`` sign in the recipe, so it knows to build ``base.txt``
    from ``base.in``.

* Now we tell ``make`` about the dependency between the requirements files.

  .. code-block:: make

      test.txt: base.txt

  This creates a dependency chain. This is an additional recipe for
  ``test.txt`` which tells ``make`` that it depends on ``base.txt``. That means
  that if ``make`` is asked to build ``test.txt``, then it should be updated if
  ``test.in`` *or* ``base.txt`` have been updated.

  If ``base.in`` is updated, then ``make`` knows that it will need to recompile
  ``base.txt`` in order to make ``test.txt``. We can see that here:

  .. code-block:: sh

      $ touch base.in       # Update timestamp on base.in
      $ make -n test.txt    # What commands will be run to build test.txt
      pip-compile -v --output-file base.txt base.in
      pip-compile -v --output-file test.txt test.in

  This is exactly what we want for requirements inheritance. If the
  requirements in our base have changed, then we want our test file to be
  recompiled too because of the ``-r base.txt`` line we added to the
  ``test.in`` file.

  Of course, this is a trivial example, but I have used
  multiple lines of dependency in Makefiles to manage multiple levels of
  inheritance in requirements files.

* Finally, a recipe to help us update requirements.

  .. code-block:: make

      check:
          @which pip-compile > /dev/null

      clean: check
          - rm *.txt

  .. **

  The ``check`` recipe will fail if ``pip-tools`` is not installed.

  The ``clean`` recipe will remove all the ``.txt`` files if the ``check``
  recipe is successful. This makes it harder to accidentally delete your
  requirements files without ``pip-tools`` already installed to be able to
  build them again.

I've explained what the Makefile above does, but not how or when you would use
it. So let's continue with some common workflow actions.


Build one or more requirements files
------------------------------------

To update all requirements use the default ``all`` recipe.

.. code-block:: sh

    $ make all

To update a particular file, ask for it by name:

.. code-block:: sh

    $ make test.txt

If ``make`` tells you that a file is up-to-date but you want to force it to
be rebuilt you should ``touch`` the ``.in`` file.

.. code-block:: sh

    $ make base.txt
    make: 'base.txt' is up to date.
    $ touch base.in
    $ make base.txt
    pip-compile -v --output-file base.txt base.in
    ...


Add a dependency
----------------

To add a dependency, locate the appropriate ``.in`` file and add the new
package name there. The version number is only required if a particular version
of the library is required. The latest version will be chosen by default when
compiling.

.. code-block:: sh

    $ cat >> base.in
    ipython
    $ make all


Update a package
----------------

In order to update a single top level package version, remove its lines from
the compiled corresponding ``.txt`` files. I tend to be quite "aggressive" with
this and remove every package that the top level package depended on using
``sed`` with a pattern match.

Given that I want to update ``ipython`` and it is not pinned in my ``.in``
file:

.. code-block:: sh

    $ sed '/ipython/d' -i *.txt
    $ make all

There is no command for this removal built into the Makefile, but potentially
it could be. Ideally, it could be provided as extra functionality by
``pip-tools``. Beware that packages often contain each other's names as
substrings so could lead to bad matching. If in doubt review your diff and
potentially remove lines from your ``.txt`` files manually.

The call to ``make all`` will reevaluate the latest version for packages that
do not have corresponding lines in the ``.txt`` file and they will be updated
as required.


Update all requirements
-----------------------

A full update of all requirements to the latest version (including updating all
packages that are not pinned in the ``.in`` file with a particular version
number) can be achieved with:

.. code-block:: sh

    $ make clean all

The ``clean`` recipe will clean out all ``*.txt`` files if you have
``pip-tools`` installed. Then the ``all`` recipe will rebuild them all in
dependency order.


Finally
-------

A tip for working with Makefiles. If you want to see what commands will be run
by a recipe, you can use the ``-n`` flag and inspect the commands that were
planned:

.. code-block:: sh

    $ make -n all

Happy requirements packing!

Update 21/11/2016
-----------------

For more information on the advantages and disadvantages of setting recursive
requirements to point at ``.in`` files or ``.txt`` files please see `this Issue
<https://github.com/nvie/pip-tools/issues/398>`_ on the ``pip-tools``
repository.

In particular, `my comment
<https://github.com/nvie/pip-tools/issues/398#issuecomment-261313647>`_
illustrates how development requirements can become out of sync with base
requirements when ``.in`` files are used in recursion which does not happen
when ``.txt`` files are used. It's for this reason, that I continue to
recommend pointing at ``.txt`` files with ``-r``.

Update 30/06/2017
-----------------

See also `this comment on GitHub
<https://github.com/jamescooke/blog/issues/9>`_ from Devin Fee for a
``Makefile`` which:

    ... corrects the annoyance ``-e file:///Users/dfee/code/zebra -> -e .``,
    making the file useful for users who don't develop / deploy from your
    directory.
