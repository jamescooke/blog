# jamescooke.info site

This repository contains content and site generation scripts for my blog at
http://jamescooke.info

The rest of this README is mainly notes to myself to install the required
packages, build and deploy the generated HTML pages to GitHub's static sites.

## Getting up and running

Pull down this blog repository as well as the
[Droidstrap](https://github.com/jamescooke/droidstrap) theme.

```sh
git clone git@github.com:jamescooke/blog
git clone git@github.com:jamescooke/droidstrap
```

Make an output folder and then set up the virtualenv.

```sh
cd blog
mkdir output
virtualenv env
source env/bin/activate
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


# License

Content in this repository is covered by the same license as the content when
published in the blog at [jamescooke.info](http://jamescooke.info/).

Licensed under [Creative Commons Attribution-ShareAlike 3.0 Unported
License](http://creativecommons.org/licenses/by-sa/3.0/deed.en_GB).
