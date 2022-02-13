Migrating from Django 1.4 to 1.5 - Lessons learned
##################################################

:date: 2013-03-29 19:00
:tags: django
:category: Code
:summary: Migrating a project from Django 1.4 to Django 1.5 had a couple of gotchas that cost me dev time.
:scm_path: content/1303-django-1.5-migration.rst

From `Ryan Kaskel <https://twitter.com/ryankask/>`_'s talk at `Django London
<https://www.meetup.com/The-London-Django-Meetup-Group/>`_ in November last
year, I guessed that upgrading the `Action Guide code
<https://github.com/jamescooke/actionguide>`_ from Django 1.4 to 1.5 might have
created some issues with users (`user models have changed in Django 1.5 to
allow more customisation
<https://docs.djangoproject.com/en/dev/releases/1.5/#configurable-user-model>`_).

However, as it turns out, the main problems were with settings and urls, the
users were fine. My main take-aways were:

Url formats have changed - now need quotes
------------------------------------------

The Django team had already updated the `url` tag to accept the path parameter
as a string, but the old syntax was still allowed. 1.4 allowed both types of
syntax, the team having provided `{% load url from future %}` for those that
wanted to update their templates to the new syntax.

Here's the warning from the `URL tag documentation
<https://docs.djangoproject.com/en/1.5/ref/templates/builtins/#std:templatetag-url>`_.

.. image:: |static|/images/url-warning.png
    :alt: Screenshot of warning from Django documentation. Warning reads:
          "Don't forget to put quotes around the function path or pattern name!

This was a reasonably easy change to implement - some search and replace and
all `url` tags can be easily hunted down and changed.


Read up on the settings - no ALLOWED_HOSTS makes 500s
-----------------------------------------------------

This was the real killer.

There is a `new ALLOWED_HOSTS settings in 1.5
<https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts>`_ required
to get Django and running in non-debug mode.

Worst thing about the implementation of this new setting is that I couldn't get
a single bit of debugging output it through `wsgi` on WebFaction - just a 500
error on every page load when I took the site out of debug mode.

I was so confused that I posted `this question on StackOverflow
<https://stackoverflow.com/questions/15605185/django-1-5-url-deprecation-warning-causes-500-error-in-webfaction-apache-wsgi/15626247>`_,
thinking the problem was `url` warnings being shown as errors and halting the
`wsgi`. In the end, just adding `ALLOWED_HOSTS` fixed everything up great.

My main problem was that I scanned the docs, tested the migration on localhost
in dev mode, and just expected everything to deploy. With Captain Hindsight,
I'd have RTFMed much harder before deploying - a lesson for the future.

Apart from that, everything works really well. **Have fun!**
