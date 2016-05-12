Django's model save vs full_clean
=================================

:date: 2015-11-15 17:00
:tags: topic:django
:category: Code
:summary: Confirming that Django can screw up your data when saving, and
          exploring why this is still the case.
:scm_path: content/1511-django-save-vs-fullclean.rst

Screwing up data
----------------

At a previous talk I gave on `"Things I wish I'd known about Django"
</things-i-wish-id-known-about-django.html>`_ there was this slide:

.. raw:: html

    <script async class="speakerdeck-embed" data-slide="6" data-id="6f327318d302437f8ccafb8da4c2cd32" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

What?
-----

I've made some experimental code in a `small Django clean vs save project
<https://github.com/jamescooke/django-clean-vs-save>`_.  It has a few models
and a `single test file
<https://github.com/jamescooke/django-clean-vs-save/blob/master/clean_vs_save/clean_vs_save/tests.py>`_
which is readable and passes.

The main take-aways are:

* Creating an instance of a Model and calling ``save`` on that instance does
  not call ``full_clean``. Therefore it's possible for invalid data to enter
  your database if you don't manually call the ``full_clean`` function before
  saving.

* Object managers' default ``create`` function also doesn't call
  ``full_clean``.

Personally I find this jarring.

Given that the developer is the customer of Django I think it conflicts with
the `principle of least astonishment
<https://en.wikipedia.org/wiki/Principle_of_least_astonishment>`_.

Why is it like this?
--------------------

The `Django documentation of Validating Objects
<https://docs.djangoproject.com/en/dev/ref/models/instances/#validating-objects>`_
is quoted in `Django ticket #13100
<http://code.djangoproject.com/ticket/13100>`_ as saying:

  Note that full_clean() will NOT be called automatically when you call your
  model's save() method. You'll need to call it manually if you want to run
  model validation outside of a ModelForm. (This is for backwards
  compatibility.)

**Ahh "backwards compatibility"?!**

It appears that phrase only lived for four months back in 2010.

* `Created 5th Jan 2010
  <https://github.com/django/django/commit/4d6c66d4d8fa63005f8ca2d3fbae195922969d13>`_

* `Removed 9th May 2010
  <https://github.com/django/django/commit/4a15dc450996b62596d74f8d98388c9e2f4a10c7#diff-5b33a9c46f488003c1846ef677f861d3L56>`_

I haven't been able to find any more specific reasons that it was added or
removed.

What next?
----------

More warnings I guess:

* Consider if you ever want to be able to call ``save`` **without**
  ``full_clean``. If the answer is 'no', then explore how you'll wrap your
  models in business logic or extend them in some way that implements this
  (with tests of course). A quick search of the internet will show you some
  Django plugins that adjust this behaviour.

* Remember that you can ruin your database when migrating if you don't call
  ``full_clean`` after the migration has changed a model but before saving. All
  migrations should be tested to ensure that they can roll-back if
  ``full_clean`` raises a ``ValidationError`` during migration.

* Check out posts like `Why I sort of dislike Django
  <http://nando.oui.com.br/2014/04/04/why_i_sort_of_dislike_django.html>`_. It
  mentions things like backwards compatibility and the ``save`` function.

Finally
-------

Thanks to `PXG <https://twitter.com/petexgraham>`_ for sharing the "Why I sort
of dislike Django" post and discussing Django project structures with me.

Thanks for reading! Comment on Github (link below) or grab me on `Twitter
<https://twitter.com/jamesfublo/>`_ with any feedback.
