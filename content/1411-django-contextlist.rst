Django Contexts and `get`
#########################

:date: 2014-11-17 20:00
:category: Testing
:summary: Found that tests on a recent project started breaking for no clear
          reason, and it turned out it was because I'd used ``get`` to retrieve
          values from Contexts.

Background
==========

If you know me, then you know that I'm an avid tester. It could even be argued
that I test too extensively as part of my day-to-day development, but that's a
post for another day.

On a recent project, a particular view started failing with the error::

    AttributeError: 'ContextList' object has no attribute 'get'

I wasn't happy with just changing the tests to work again, so I dug down into
why they started failing.


TLDR;
=====

To get a value from a Context returned to you by the Django Test Client, then
it's better to use the ``[]`` operator, than the ``get`` method.

For example:

.. code-block:: python

    # It's better to use []
    self.assertEqual(response.context['name'], 'Homer')

    # ...than to use get
    self.assertEqual(response.context.get('name'), 'Homer')


Reason
======

It turns out that the problem was to do with another developer on the project
changing how the template for the view was generated - from a single template,
to a couple of templates using Django's template inheiritance and the ``{%
extends %}`` template tag.



Grab me on `Twitter <https://twitter.com/jamesfublo/>`_ to discuss testing.

Thanks for reading.
