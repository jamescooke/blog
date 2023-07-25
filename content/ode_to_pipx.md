Title: An Ode to pipx
Date: 2023-07-25 19:00
Category: Python
Tags: language:python
Summary: Using `pipx` has improved my daily development experience considerably.

Oh pipx, how I love thee... 🎵

Using pipx means I can have Python packages installed and executable on my path
much more easily than in the past. That's changed my general development
experience for the better. Here's how...

## Before pipx

When I wanted to make a Python package (like IPython) available on the command
line in my Linux environment, I would get hacky... Using `virtualenv` and
boilerplate `bash` scripts I would manage package installs, and then wrap them
in a script to make them available on my `PATH`.

The main reason for using virtual environments for these projects and tools is
to keep my Ubuntu global Python environment clean: Not all Python tools should
just be thrown in there. Separation is important, not least because each
package may have conflicting package requirements and may not be able to be
installed together.

As an example, to make IPython runnable on the command line I would:

* Create a directory for `ipython` in `~/opt`.
* Build a virtual environment inside it and install `ipython` there.
* Add a wrapper executable script called `ipython` which was then callable on
  my shell's `PATH`.

That script looked like:

```sh
#!/bin/bash

set -eo pipefail

~/opt/ipython/venv/bin/ipython
```

### Disadvantages

There were many issues with this - not least the problems with managing the
resulting stack of venv and wrappers as the number of Python tools I wanted on
my path grew.

Yes - these could be handled with Ansible (I like to build and manage my
machines with Ansible), but there always seems to be a lag between the time I
"need" a new thing on my command line, and when I manage to get it wired into
Ansible correctly.

Upgrades also become hard - where were all those manually managed tools? Which
ones should I update?

A small, but niggling, disadvantage for using the wrapper script to run local
private tools: I found is that it was hard to keep "development" and
"production" separate. I'd rarely re-create the private code repository so I
could run a version on shell `PATH` separate from the development directory.
No, instead, the wrapper script I'd throw in would be calling the development
directory. This would often mean that when I was trying to do small fixes or
improvements, I would often accidentally break my tool, or make it unusable in
some way. Annoying when you're trying to update some accounts and you've broken
your bank account parsing tool.

## Switching to pipx

I installed pipx into the user virtual environment on my Ubuntu machine as
per [the instructions](https://pypa.github.io/pipx/).

```sh
python3 -m pip install --user pipx
```

Then, installing IPython was as simple as:

```sh
pipx install ipython
```

Everything just worked and IPython was installed successfully. Pipx even warned
me that there was a previous executable on my path (my previous crappy wrapper
script).

### Better dev life

Now I use `pipx` to install, manage the virtual environment and expose
packages' endpoints on my shell's `PATH`.

* 🙅 Gone are the wrapper scripts and manually built virtual environments.
* 🙅 Gone are the multiple directories of Python apps, some in `~/opt` some in
  `~/active` (my usual working path). Along with their Make recipes for
  managing virtual environments and upgrades.
* 🙅 Gone is the need for orchestration scripts and Make recipes to "know" the
  particular directory and virtual environment a package is installed in. Pipx
  can upgrade everything with `pipx upgrade-all`.

## ✅ Public packages

I now install all my favourite, regularly used, public packages with pipx, so
they're available on the command line.

My favourite public packages currently installed are:

* [devpi-server](https://github.com/devpi/devpi) to save a tonne of downloads
  when recreating Tox environments.
* [flit](https://flit.pypa.io/en/stable/) for packaging.
* [frogmouth](https://github.com/Textualize/frogmouth/) - my new favourite
  Markdown tool.
* [hledger-utils](https://pypi.org/project/hledger-utils/) for helping with our
  family accounts.

## ✅ Personal private packages

I've got baggage - and it lives in private repositories: A suite of personal
tools I've built up over the years used for all sorts of tasks, from filing
downloads into correct directories, to managing my work time, to bookkeeping
our family accounts.

With pipx these are now executable from anywhere in my shell, with none of the
previous overhead and boilerplate mentioned above.

These personal private packages are a little harder for me to get into pipx,
but only because I'm lazy - if you've done your proper packaging, then you're
probably already set.

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

### Try installing from `.`

### Add pyproject.toml with entrypoints

```sh
flit init
```

Add entry points

Add packages that are required to run the package

> TODO think about "Tox for smoke testing your package"

Best of all, the pipx install is a **clone** of the package. That means I can
continue to work on it in my `~/active` directory, making breaking changes as
required, while the installed version continues to operate, isolated in its
pipx-managed install directory.

## Next steps

Some things I'm not sure about yet.

### Installing from private GitLab

So next step is to remove the copy of the project in my `~/active` directory
entirely and just use the `pipx` installed version. This means that I get more
cleanliness in my development environment - no need to keep directories around
in order to provide runnable Python code any more.

> TODO install from private gitlab.

### Managing all this with Ansible

[Ansible `pipx`
module](https://docs.ansible.com/ansible/latest/collections/community/general/pipx_module.html)
in Ansible galaxy.

## Thanks

Thanks for reading.

Thanks to Brian and Michael for "nagging" bloggers that it doesn't have to be
perfect - just write the thing and put it out there.

Thanks to Fosstodon folks for tooting new and interesting things that inspired
me to try out these things and get them working for myself.
