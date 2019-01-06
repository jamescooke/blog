# jamescooke.info blog

This repository contains content and site generation scripts for my blog at
https://jamescooke.info

## Blog post comments

My blog doesn't run a commenting system, but feedback and conversation are very
welcome. There are three main channels:

* Drop me an email on `hi AT jamescooke DOT info`.

* Raise an [Issue on GitHub](https://github.com/jamescooke/blog/issues/new) and
  I'll reply as soon as I can. Issues that are comments have their own ["blog
  comment"](https://github.com/jamescooke/blog/issues?q=is%3Aissue+label%3A%22blog+comment%22)
  label for easy access.

***

The rest of this README is mainly notes to myself to install the required
packages, build and deploy the generated HTML pages to GitHub's static sites.

## Getting up and running

In addition to this repository,
[Droidstrap](https://github.com/jamescooke/droidstrap) theme and [Pelican
plugins](https://github.com/getpelican/pelican-plugins) are required.

```sh
git clone git@github.com:jamescooke/blog
git clone git@github.com:jamescooke/droidstrap
git clone --recursive https://github.com/getpelican/pelican-plugins
```

Make an output folder and then set up the virtualenv.

```sh
cd blog
mkdir output
make -f Bakefile venv
make -f Bakefile install
```

## Writing and testing

While in virtualenv, run dev server.

```sh
. venv/bin/activate
make devserver
```

Hit [localhost](http://localhost:8000/).

## Publishing

Commit content and images as required, push to master. Then...

```sh
make github
```

The GitHub pages plugin does some funky stuff with the `gh-pages` branch. This
can be cleaned up using `make clean_github`.

## Requirements

Requirements are managed with ``pip-tools``.

# License

Content in this repository is covered by the same license as the content when
published in the blog at [jamescooke.info](https://jamescooke.info).

Licensed under [Creative Commons Attribution-ShareAlike 3.0 Unported
License](https://creativecommons.org/licenses/by-sa/3.0/deed.en_GB).
