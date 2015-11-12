# jamescooke.info blog

This repository contains content and site generation scripts for my blog at
http://jamescooke.info/

## Blog post comments

My blog doesn't run a commenting system, but feedback and conversation are very
welcome. There are three main channels:

* Drop me an email on `hi AT jamescooke DOT info`.
* [Tweet me](https://twitter.com/intent/user?screen_name=jamesfublo).
* Drop a github comment on the content. All blog posts are in the [content
    folder](content). Alternatively raise an Issue and I'll reply as soon as I
    can.

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
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```

## Writing and testing

While **still in the virtualenv**, build the HTML and run dev server.

```sh
make html
make devserver
```

Hit [localhost](http://localhost:8000/).

## Publishing

Commit content and images as required, push to master. Then...

```sh
make publish
make github
```

All good in the hood.

## Requirements

Requirements are managed with ``pip-tools``.

# License

Content in this repository is covered by the same license as the content when
published in the blog at [jamescooke.info](http://jamescooke.info/).

Licensed under [Creative Commons Attribution-ShareAlike 3.0 Unported
License](http://creativecommons.org/licenses/by-sa/3.0/deed.en_GB).
