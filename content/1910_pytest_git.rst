Pytest's cache and gitignore
============================

:date: 2022-12-19 15:00
:tags: language:python, git
:category: Code
:summary: Sanity checking Pytest's ``.gitignore`` files.
:scm_path: content/1910_pytest_git.rst

This post is about sanity checking. It was written at the end of 2019, but not
published until the end of 2022. The underlying change to Pytest's cache
directories was made in ``3.8.1``, released at the end of 2018.

TL;DR 🥱
---------

* You can check any path, real or imaginary, with ``git check-ignore`` to see
  if Git will ignore it or not.

* Pytest prevents its cache directory ``.pytest_cache`` from getting into Git
  repositories by adding a ``.gitignore`` file inside them.

The (long) story 📜
-------------------

While working on a project using Pytest, ``pytest --lf`` was not selecting all
possible tests.

The ``--lf`` flag tells Pytest to run `the tests that failed in the last run
<https://docs.pytest.org/en/latest/cache.html#rerunning-only-failures-or-failures-first>`_
and those test IDs are stored in Pytest's cache.

To ensure that I started from a clean place, I went to clean out the
``.pytest_cache`` directory. But while I was looking at that directory, I had a
mild panic - I had completely forgotten to add it to project's ``.gitignore``
file!

Had I accidentally committed the ``.pytest_cache`` dir?!

Was this why ``pytest --lf`` was being strange?!

Not in Git
..........

Firstly, I was able to reassure myself that I'd *not* accidentally committed
the cache directory: ``git log`` can accept a path, so when ``git log --
.pytest_cache`` came back empty, this was reassuring. It was not committed to
the repo!

However, there was no entry for ``.pytest_cache`` in ``.gitignore``.

I usually populate the ``.gitignore`` for Python projects by lifting the lines
that I want from the `Github gitignore repo
<https://github.com/github/gitignore/blob/master/Python.gitignore>`_, but I'd
forgotten to copy over the line for ``.pytest_cache``.

Why is the ``.pytest_cache`` directory being ignored by Git if I've not written
a pattern for it into ``.gitignore``?

Checking ignored files
......................

My guess was one of the existing patterns in ``.gitignore`` might be matching
the ``.pytest_cache`` path. To check this I went through deleting lines from
the file until it was empty. But even with an empty ignore file,
``.pytest_cache`` still did not get picked up by Git!

Then I went and found that there is a super-helpful ``git check-ignore``
command. You can read some of the background of this command on `Stack Overflow
<https://stackoverflow.com/a/12168102/1286705>`_. This can be used to check
what Git ignore thinks of a path.

So now I can call::

    git check-ignore -v .pytest_cache/

And get back::

    .pytest_cache/.gitignore:2:*    .pytest_cache/

This means:

* There is a file ``.pytest_cache/.gitignore``.

* Line 2 of that file is ``*``.

* This rule is being applied to ``.pytest_cache/``.

So - Pytest creates its own ``.gitignore`` file in the cache to prevent it
being included! Phew, what a journey! 😪

A bit more investigation
........................

So now we have an opportunity to learn a little bit about Pytest...

From some searching, I found that the inclusion of a ``.gitignore`` file in
Pytest's cache directories was a feature:

* Introduced in `Pull #3982: Ignore pytest cache
  <https://github.com/pytest-dev/pytest/pull/3982>`_.

* To solve `Issue #3286: .pytest_cache is showing up in projects git repos
  <https://github.com/pytest-dev/pytest/issues/3286>`_.

Previously, Pytest had renamed its cache directory from ``.cache`` to
``.pytest_cache``. As a result, on projects where maintainers hadn't updated
their ignore files, the new cache directories had been committed by accident.

In looking at the Pytest team's response, what's interesting to me is the
trade-off between:

* Pytest developers do nothing. Let Pytest users update their ``.gitignore``
  files or other SCM ignore methods, or...

* Pytest developers take some action. Prevent the folder being added to SCM
  systems or some other fix.

In the discussion on the Issue, `this comment
<https://github.com/pytest-dev/pytest/issues/3286#issuecomment-393142058>`_
shows the idea of a ``.pytest_cache/.gitignore`` file coming into being:

    another devious idea - if we add a ``.gitignore`` with the content ``*``
    then the folder is protected as well and people dont need to track manually

But all decisions have consequences.

Less might be more
..................

For me I would prefer to follow `the Zen of Python
<https://www.python.org/dev/peps/pep-0020/#id3>`_:

    Explicit is better than implicit.

I would vote for: Let Pytest users update their ignore mechanisms.

This would mean:

* Pytest SCM users learn that ``.pytest_cache`` exists and add it to their
  ``.gitignore`` or similar.

* Confusion is avoided because no directories are unexpectedly ignored by Git.
  (Confusion as you can see in my case above and also in `this issue
  <https://github.com/pytest-dev/pytest/issues/4886>`_.)

* Other side effects do not occur, like this ones mentioned in the issue above
  regarding Debian packaging or search.

To the wider open source issue, I think that projects that do less will last
better than projects that do too much. I would generally take trade-offs where
less is done rather than more.

Reflection 2022
---------------

Much of this post was written in 2019, much has happened, my confusion has
lessened.

If you ask "did the Pytest team do the right thing by adding ``.gitignore`` to
the newly named ``.pytest_cache`` directories?", then my answer is **yes**.

It seems to have been a successful strategy and is even `used by mypy
<https://github.com/python/mypy/pull/8193>`_ with a hat-tip to Ronny
Pfannschmidt's original comment suggesting the idea.

While editing this post, I found `two
<https://github.com/pytest-dev/pytest/issues/4886#issuecomment-470498105>`_
`quotes
<https://github.com/pytest-dev/pytest/issues/4886#issuecomment-469877128>`_
from Ronny that I'll end with:

    we would be more than happy to have a better way (like xdg)

    but lets be realistic here - the added .gitignore protects beginner uses
    from a very common mistake, that's why its there

    its a practical solution to a practical problem and has a interference
    component

...

    from my pov its an absolutely acceptable tradeoff to prevent a lot of
    developer pain by inflicting a extra step on package maintainers

Nice one Pytest team for looking after new developers! 🙌
