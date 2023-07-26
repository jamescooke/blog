Title: How to Pipx-ify a Private Package
Date: 2023-08-02
Category: Python
Tags: language:python
Summary: A quick hacky guide on how to install private packages into pipx so
    you can use your home-rolled tools on the command line without boilerplate.
Status: draft

## Installing local private packages

Given I've usually cut corners to get things working, my private tools are
often runnable with the Python installed in the tool's virtual environment:

```py
python some_tool.py [args]
```

And if I'm _really_ lucky, then past-me has done a Python main with `-m`.

```py
python -m some_tool [args]
```

Either way, getting them working with pipx I found pretty easy.

### Try installing from the directory

First try installing the private package you want to make runnable from its
currently installed directory.

If you want `mypackage` in `~/active` to be installed by pipx, then point it at
the directory:

```sh
pipx install ~/active/mypackage
```

If this "Just Works ™️" for you, then you're all set. 🎉


However, I'm often lazy with my own code, so pipx can't find what to install:

```
ERROR: Directory '/home/james/active/mypackage' is not installable. Neither 'setup.py' nor 'pyproject.toml' found.
Cannot determine package name from spec '/home/james/active/mypackage'. Check package spec for
errors.
```

### Add pyproject.toml

Given I've already installed [Flit](https://flit.pypa.io/en/stable/) using
pipx, it's now really easy to use Flit as the build system in the project. Just
run `init` and follow the prompts for a "standard" `pyproject.toml` to be
created for you:

```sh
flit init
```

This will give you a default `pyproject.toml` file.

You'll also need to add a docstring to your projects `__init__.py` file, something like:

```py
"""
This is mypackage and it's amazing
"""

__version__ = "0.1.0"
```

Now retry installing with `pipx install` and you'll get a new error:

```
No apps associated with package mypackage or its dependencies. If you are attempting to install a library, pipx should not be used. Consider using pip or a similar tool instead.
```

### Add entry points

Pipx is complaining because it doesn't look like there's an executable in
"mypackage" - and that makes sense because there are no entry points in the
`pyproject.toml` file.

To cut a long story short, [entry points are complex
beasts](https://packaging.python.org/en/latest/specifications/entry-points/#entry-points).
Here's an example of the kind of thing I've hacked into "mypackage":

```toml
[project.scripts]
mypackage = "mypackage:cli.do"
```

This will make a `mypackage` executable available on the command line. It tells
pipx to point at the `do()` callable in the `cli` module (I think - TBH I just
hit it until it works).

Now try installing again (note: I'm lazily in the `~/active/mypackage`
directory and just using `.`), and it _should_ work:

```sh
pipx install . --python=python3.11
```

```
  installed package mypackage 0.1.0, installed using Python 3.11.4
  These apps are now globally available
    - mypackage
done! ✨ 🌟 ✨
```

### Oh no - moar packages!

Now I can run `mypackage` from wherever I want on the command line:

```sh
mypackage --help
```

But there's a snag:

```
Traceback (most recent call last):
  File "/home/james/.local/bin/mypackage", line 5, in <module>
    from mypackage import cli
  File "/home/james/.local/pipx/venvs/mypackage/lib/python3.8/site-packages/mypackage/cli.py", line 3, in <module>
    import rich_click as click
ModuleNotFoundError: No module named 'rich_click'
```

Pipx hasn't installed any dependencies of mypackage - so it won't run in it's
nice, new, clean pipx virtual environment!


Best of all, the pipx install is a **clone** of the package. That means I can
continue to work on it in my `~/active` directory, making breaking changes as
required, while the installed version continues to operate, isolated in its
pipx-managed install directory.

