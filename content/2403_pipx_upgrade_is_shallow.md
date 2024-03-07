Title: Pipx's upgrade is shallow, let's go deeper
Date: 2024-03-07
Category: Python
Tags: language:python
Summary: Software installed in pipx's managed virtual environments can get
    stale. How can we update those packages _and_ their dependencies?

pipx has been managing my Python tools for almost a year.

But those tools are getting stale - new versions are out - I need to upgrade.

## 💪 Let's upgrade this

One of my favourite and most used Python tools installed in pipx is
[Frogmouth](https://pypi.org/project/frogmouth/). While working on some
documentation, I think I've spotted a bug in some Markdown rendering. So before
I report the bug, let's ensure I've got the latest version.

Upgrading "Is Easy ™️". Just use `pipx upgrade`:

```sh
pipx upgrade frogmouth
```

We get a spinner, and then:

```
frogmouth is already at latest version 0.9.2 (location: /home/james/.local/pipx/venvs/frogmouth)
```

Success! Nothing to do, end of blog post.

...

## 🔎 Let's check

Frogmouth is using [Textual](https://pypi.org/project/textual/) and
[rich](https://pypi.org/project/rich/) under the hood - so if I want to make
sure I've got the latest Markdown code, I need to ensure they've been upgraded
too.

Let's ask `pip` to tell us all versions of packages in the `frogmouth` virtual
environment:

```sh
pipx runpip frogmouth list
```
```
Package            Version
------------------ ---------
anyio              3.7.1
certifi            2023.7.22
frogmouth          0.9.2        👈 Here's Frogmouth at the latest version
h11                0.14.0
httpcore           0.17.3
httpx              0.24.1
idna               3.4
importlib-metadata 6.8.0
linkify-it-py      2.0.2
markdown-it-py     3.0.0
mdit-py-plugins    0.4.0
mdurl              0.1.2
pip                24.0
pkg_resources      0.0.0
Pygments           2.16.1
rich               13.5.2       👈 rich is at 13.7.1 on PyPI
setuptools         69.1.1
sniffio            1.3.0
textual            0.43.2       👈 Textual is at 0.52.1 on PyPI
typing_extensions  4.7.1
uc-micro-py        1.0.2
wheel              0.42.0
xdg                6.0.0
zipp               3.16.2
```

Uho - rich and Textual didn't get updated by doing `pipx upgrade`.

## 🤔 This kinda makes sense

When we have a virtual environment for a project and we run `pip upgrade`, it
_just_ upgrades the package we request. It only upgrades dependencies if they
conflict with the newly upgraded package. This is called the "only-if-needed"
strategy and is [documented in the pip User
Guide](https://pip.pypa.io/en/stable/user_guide/#only-if-needed-recursive-upgrade).

But, given I'm a [pip-tools](https://pypi.org/project/pip-tools/) addict, I
rarely call `pip` directly. Usually I blow away all of a project's
requirements, rebuild them with `pip-compile` and then install all the new
freshness with `pip-sync`.

How can I get this "everything new" behaviour with `pipx`? I think there are
two options...

## Option 1: Tell pip to be eager

Also listed in the pip User Guide is the "eager" option which:

> upgrades all dependencies regardless of whether they still satisfy the new
> parent requirements.

This sounds like what I'm looking for.

And, luckily, `pipx upgrade --help` shows us just what we need:

```
--pip-args PIP_ARGS   Arbitrary pip arguments to pass directly to pip install/upgrade commands
```

Let's try it by passing `--upgrade-strategy=eager`:

```sh
pipx upgrade --pip-args=--upgrade-strategy=eager frogmouth
```

This, unfortunately, gives very little output regarding the packages being
updated. So let's check them again with `pip list` (this time just grepping for
'rich' and 'textual'):

```sh
pipx runpip frogmouth list | grep -E '^rich|^textual'
```
```
rich               13.7.1   🎉 Yay - upgraded to latest.
textual            0.43.2   😞 boo - not upgraded to latest.
```

### 😬 Textual ain't gunna upgrade

After "some" digging, it turns out that Textual isn't going to upgrade when
installing / upgrading Frogmouth. That's because Frogmouth has a [caret
requirement](https://python-poetry.org/docs/dependency-specification/#caret-requirements)
in [its `pyproject.toml`
file](https://github.com/Textualize/frogmouth/blob/main/pyproject.toml#L31)
which restricts Textual from being upgraded beyond `0.43`.

I only discovered this after pulling out `pip-tools` and running a clean
compile of the current Frogmouth requirements and diffing them to the output of
`pipx runpip frogmouth list`.

Personally, I think this kind of pinning is frustrating, especially in [zero
versioned](https://0ver.org/) software. If something breaks I can apply any
pins required to get them to work - I don't need the upstream maintainer to do
it for me. That just creates slowness and unnecessary confusion.

Anyway - back to the upgrades...

## Option 2: Hit it with a reinstall

There is _another_ way. That's to ask pipx to do a reinstallation of the
software. As per `pipx reinstall --help`:

> Package is uninstalled, then installed with pipx install PACKAGE with the
> same options used in the original install of PACKAGE.

Warning: this is a bit of a lie. The `--python` option is not kept when doing
reinstall. But, this _does_ allow for new versions of Python to be used after
reinstalling.

Given that I'm not using the default Python version for pipx installs, I always
have to pass in my preferred Python:

```sh
pipx reinstall frogmouth --python=python3.12
```
```
uninstalled frogmouth! ✨ 🌟 ✨
  installed package frogmouth 0.9.2, installed using Python 3.12.2
  These apps are now globally available
    - frogmouth
done! ✨ 🌟 ✨
```

And rich and Textual got to the same versions as before with "eager":

```sh
pipx runpip frogmouth list | grep -E '^rich|^textual'
```
```
rich               13.7.1
textual            0.43.2
```

## Which is best?

My guess is you should use what you think is best for your workflow.

I'm aggressive with my upgrading, so I'm happy with the `pipx reinstall` route.
This also may give cleaner virtual environments since we shouldn't get any
hanging dependencies in the scenario that a package stops using a particular
dependency.

Also, during my experimentation, I accidentally installed a package off PyPI
called "eager" 🤦. Luckily it didn't run and the source doesn't look malicious
to my trusting eye. But it's this kind of mistake that's nicely cleaned up
every time the virtual environment is recreated with `reinstall`. 😅
