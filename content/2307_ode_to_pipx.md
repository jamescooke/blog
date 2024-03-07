Title: An Ode to pipx
Date: 2023-07-26 21:00
Category: Python
Tags: language:python
Summary: Using pipx has improved my daily development experience considerably.

Oh pipx, how I love thee... 🎵

Using pipx means I can have Python packages installed and executable on my path
much more easily than in the past. That's changed my personal _and_ work
development experience for the better. Here's how...

## Before pipx

When I wanted to make a Python package (like IPython) available on the command
line in my Linux environment, I would get hacky... Using `virtualenv` and
boilerplate `bash` scripts I would manage package installs, and then wrap them
in a script to make them available on my `PATH`.

As an example, to make IPython runnable on the command line I would:

* Create an IPython directory in my user's `opt` dir: `~/opt/ipython`.
* Build a virtual environment inside it.
* Activate the virtual environment and install IPython there with `pip`.
* Add a wrapper executable script called `ipython` which was then callable on
  my shell's `PATH`.

That script looked like:

```sh
#!/bin/bash

set -eo pipefail

~/opt/ipython/venv/bin/ipython
```

> A side note about Python environments:
> The main reason for using virtual environments for these projects and tools is
> to keep my Ubuntu global Python environment clean: Not all Python installed
> packages can or should just be thrown in there. Separation is important, and
> sometimes required, not least because each package may have conflicting package
> requirements and may not be able to be installed together.

### Disadvantages of these hacks

There were a growing number of issues with the hacky approach above - not least
the problems with managing the resulting stack of venv and wrappers as the
number of Python tools I wanted on my path grew.

Yes - these could be handled with Ansible (I like to build and manage my
machines with Ansible), but there always seems to be a lag between the time I
"need" a new thing on my command line, and when I manage to get it wired into
Ansible correctly.

Upgrades also became hard - where were all those manually managed tools? Which
ones should I update?

A small, but niggling, disadvantage for using the wrapper script to run local
private tools: I found is that it was hard to keep "development" and
"production" separate. I'd rarely re-create the private code repository so I
could run a version on shell `PATH` separate from the development directory.
No, instead, the wrapper script would call the development directory directly.
Often when I was trying to do small fixes or improvements, I would accidentally
break my tool, or make it unusable in some way. Annoying when you're trying to
update some accounts and the bank account parsing tool is crashing because
you're half way through updating it.

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

Everything just worked and IPython was installed successfully. pipx even warned
me that there was a previous executable on my path (my previous crappy wrapper
script).

### A better dev life

Now I use pipx to install, manage the virtual environment and expose packages'
endpoints on my shell's `PATH`.

* 🙅 Gone are the wrapper scripts and manually built virtual environments.
* 🙅 Gone are the multiple directories of Python apps, some in `~/opt` some in
  `~/active` (my usual working path). Along with their Make recipes for
  managing virtual environments and upgrades.
* 🙅 Gone is the need for orchestration scripts and Make recipes to "know" the
  particular directory and virtual environment a package is installed in. pipx
  can upgrade everything with `pipx upgrade-all`.

## ✅ Public packages

I now install all my favourite, regularly used, public packages with pipx so
they're available all the time on the command line.

My favourite public packages currently installed are:

* [devpi-server](https://github.com/devpi/devpi) to allow Tox to install
  packages without having Pip call PyPI.
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

> I've got a follow-up post about making your private packages installable with
> pipx which I'll publish soon.

## Next steps

Some things I'm not sure about yet.

### Private packages from private repositories

My current pipx install workflow for private packages depends on having them
cloned to a local directory, and then calling `pipx install [path]` to install
from there.

I would like it if I could install my private packages directly from their
private GitLab repository without manually cloning first - I'm pretty sure pipx
_can_ do this, I've just not hacked around enough with the invocation.

This improvement would mean that I would just use a pipx install of my private
packages, and that means more cleanliness in my development environment - no
need to keep directories around in order to provide runnable Python code any
more.

### Managing all this with Ansible

As I mentioned I usually build and manage my machines with Ansible. I need to
invest some time in catching my Ansible playbooks with my current machine
states and the [Ansible `pipx`
module](https://docs.ansible.com/ansible/latest/collections/community/general/pipx_module.html)
in Ansible galaxy looks particularly helpful.

## 🙏 Thanks

Thanks for reading.

Thanks to [Brian and Michael's
coverage](https://pythonbytes.fm/episodes/show/342/dont-believe-those-old-blogging-myths)
of [Julia Evans's "Some blogging
myths"](https://jvns.ca/blog/2023/06/05/some-blogging-myths/) post... For
"nagging" bloggers that it doesn't have to be perfect - just write the thing
and put it out there.

Thanks to [Fosstodon folks](https://fosstodon.org/) for tooting the new and
interesting things, that, in turn, inspire me to try out these things and get
them working for myself.
