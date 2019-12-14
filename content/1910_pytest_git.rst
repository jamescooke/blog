Pytest_cache and gitignore
==========================

:date: 2019-10-24 23:00
:tags: language:python
:category: Code
:summary: Sanity checking Pytest's gitignore file.
:scm_path: content/1804-pysyncgateway.rst

This post is about sanity checking.

TL;DR
-----

* Pytest prevents its ``.pytest_cache`` directory from getting into Git
  repositories by adding a ``.gitignore`` file inside it.

* You can check any path, real or imaginary, with ``git check-ignore`` to see
  if it will be ignored.

The story
---------

This week I was working on a project using Pytest.

The problem I was having was that ``pytest --lf`` was not selecting all
possible tests. The ``--lf`` flag tells Pytest to run `the tests that failed in
the last run
<https://docs.pytest.org/en/latest/cache.html#rerunning-only-failures-or-failures-first>`_
and those test IDs are stored in Pytest's cache.

To ensure that I started from a clean place, I went to clean out the
``.pytest_cache`` directory. But while I was looking at that directory, I had a
mild panic - I had completely forgotten to add it to project's ``.gitignore``
file!

Had I accidentally committed it?! Was this why ``pytest --lf`` was being
strange?!

Firstly I was able to reassure myself that I'd not accidentally committed it:
``git log`` can accept a path, so when ``git log -- .pytest_cache`` came back
empty, this was reassuring. It was not committed to the repo!

However, it was not in ``.gitignore``.

I usually populate the ``.gitignore`` for Python projects by lifting the lines
that I want from the Github ``gitignore`` repo:
https://github.com/github/gitignore/blob/master/Python.gitignore . I can see
the line in there for ``.pytest_cache`` but I'd forgotten to add it.

Why is the ``.pytest_cache`` directory being ignored by Git if I've not written
a pattern for it into ``.gitignore``?

At first I thought that one of the existing patterns might be matching the
``.pytest_cache`` path. To check this I went through deleting lines from the
``.gitignore`` file until it was empty, but ``.pytest_cache`` still did not
appear!

Then I went and found that there is a super-helpful ``git check-ignore``
command. (You can read some of the background of this command on Stack Overflow
: https://stackoverflow.com/a/12168102/1286705)

So now I can run ::

    $ git check-ignore -v .pytest_cache/

And get back::

    .pytest_cache/.gitignore:2:*    .pytest_cache/

What does this mean? This took me a few minutes and more prodding to grok, but,
it is saying that there is a file ``.pytest_cache/.gitignore`` and line 2 of
that file is ``*``. This is the rule that is being applied.

So - Pytest creates its own ``.gitignore`` file in the cache to prevent it
being included! Phew, what a journey!

So now we have an opportunity to learn a little bit about Pytest. From some
searching, I found that this feature was introduced in #3982
https://github.com/pytest-dev/pytest/pull/3982. This change does not appear in
the CHANGELOG (https://docs.pytest.org/en/latest/changelog.html) so it can be
hard to search it up.

Adding ``.gitignore`` with ``*`` to ``.pytest_cache`` was a solution to the
problem of ``.pytest_cache`` directories appearing in projects after it was
renamed from ``.cache``. https://github.com/pytest-dev/pytest/issues/3286

What's interesting to me is the trade-off between:

* Pytest developers doing nothing. Let users of the tool update their
  ``.gitignore`` files or other SCM ignore methods. And..

* Pytest take some action to prevent the folder being added to SCM systems.


This comment shows the idea of a ``.pytest_cache/.gitignore`` file coming into being: https://github.com/pytest-dev/pytest/issues/3286#issuecomment-393142058

    another devious idea - if we add a .gitignore with the content * then the
    folder is protected as well and people dont need to track manually

But all decisions have consequences. For me I would prefer to follow the Zen of
Python "Explicit is better than implicit"
https://www.python.org/dev/peps/pep-0020/#id3 and let Pytest users update their
ignore mechanisms.

This would mean that:

* Pytest users learn that ``.pytest_cache`` exists and add it to their
  ``.gitignore`` or similar.

* There is reduced confusion (as you can see in my case above) when a directory
  is unexpectedly ignored by Git.

* Other side effects do not occur, like this one documented about Debian
  packaging https://github.com/pytest-dev/pytest/issues/4886.

To the wider open source issue, I think that projects that do less will last
better than projects that do too much. I would generally take trade-offs where
less is done rather than more.


[1] If you don't know this super helpful ``--lf , --last-failed`` flag, then
it's great for running against large test suites where changes you're working
on affect a number of tests.
