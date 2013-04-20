Setting up this homepage with Pelican
#####################################

:date: 2013-01-20 17:25:00
:tags: github, python, pelican
:summary: Using Pelican to generate this blog, a move away from Jekyll and to some pure Python.

This page has been through a lot in the last ten years.

Since starting work at `Quibly <http://quib.ly>`_, I've had a lot more time to code and it's exactly what I wanted, hopefully it'll continue. The result of that is that I've got more to write about... The code that I develop at work, fixes I make to open source libraries and general things I learn, primarily about Python and web - hopefully all valuable and worth sharing.

I'm experimenting with `Pelican <https://github.com/getpelican/pelican>`_ - a static blog generator written in Python. It's excellent and noticably easier than Jekyll - probably because I'm much more clued up in Python than Ruby. I'm lazy, so I'm hosting the outputted static files in the ``gh-pages`` branch of the `blog's repository <https://github.com/jamescooke/blog/>`_ to take advantage of `GitHub Pages' free hosting features <http://pages.github.com/>`_ - thanks GitHub!

In addition, I found `this article by David Fischer <http://www.davidfischer.name/2012/12/quick-note-pelican-github/>`_ very helpful. Particularly the suggestion of adding the ``CNAME`` copy command to the ``Makefile`` to get GitHub Pages one configuration requirement and ``gph-import`` working nicely together. Plus David pointed out that Pelican already has a ``github`` target in the ``Makefile`` which I hadn't noticed and is now what I use to push articles live.

All in all - great and simple.
