Title: How to Pipx-ify a Private Package
Date: 2023-08-02
Category: Python
Tags: language:python
Summary: A quick and hacky guide on how to install private packages with Pipx
    so you can use your home-rolled tools on the command line without
    boilerplate.

Previously I wrote [an "Ode to Pipx"]({filename}/2307_ode_to_pipx.md):

> Oh pipx, how I love thee... 🎵

In that post, I mentioned I'd hacked together some private packages to be
installed on the command line using [pipx](https://pipx.pypa.io/stable/).

## Context

My private packages are often:

* In a private repository on a local machine. Often (but not always) I've
  pushed that to my private [Forgejo instance](https://forgejo.org/) on a
  raspberry pi.
* Developed in earnest when I need to fix a problem: "I just need an X to do
  Y", but after that I don't really change the code more than every six months
  or so.
* Carrying a single `requirements.in` requirements file with all (dev, test,
  production) dependencies lobbed in. This is compiled to `requirement.txt` with
  `pip-tools`.
* Those requirements get installed in a virtual environment in the same
  directory as the tool's checked out repo directory.
* They get used often - at least a couple of times a week usually.
* They get called from various paths on my system.

Given the above, I would usually then craft boilerplate scripts to allow the
tool to be used from all over my system.

But now, with Pipx, that need for boilerplate would be gone _if_ I could
install the private package with Pipx...

If my list above is resonating with your usual Python set-up, you've probably,
like me, skipped the packaging part of your "super helpful tool". Instead, I'm
invoking the tool with the Python installed in the virtual environment:

```py
python some_tool.py [args]
```

And if I'm _really_ lucky, then past-me has done a Python main with `-m`.

```py
python -m some_tool [args]
```

From here, this is how I've got these package working with Pipx.

## First, try installing from package directory

First try installing the private package you want to make runnable from its
currently installed directory.

If you want `mypackage` in `~/active` to be installed by Pipx, then point it at
the directory:

```sh
pipx install ~/active/mypackage
```

If this "Just Works ™️" for you, then you're all set. 🎉

As I've explained I'm often lazy with my own code, so Pipx can't find what to
install:

```
ERROR: Directory '/home/james/active/mypackage' is not installable. Neither 'setup.py' nor 'pyproject.toml' found.
Cannot determine package name from spec '/home/james/active/mypackage'. Check package spec for
errors.
```

## Add pyproject.toml

Given I've already installed [Flit](https://flit.pypa.io/en/stable/) using
Pipx, it's now really easy to use Flit as the build system in the project. Just
run `init` and follow the prompts for a "standard" `pyproject.toml` to be
created for you:

```sh
flit init
```

This will give you a default `pyproject.toml` file.

You'll also need to add a docstring to your projects `__init__.py` file,
something like:

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

## 😊 Big wins

Personally I'm loving pipx. And this hacky "workflow" has really helped me to
make utilities available for myself on the command line, without the need for
boilerplate wrapper scripts.

Best of all, the pipx install is a **clone** of the package. That means I can
continue to work on it in my `~/active` directory, making breaking changes as
required, while the installed version continues to operate, isolated in its
pipx-managed install directory.

Happy hacking!
