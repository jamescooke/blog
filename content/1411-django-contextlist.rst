Django Contexts and `get`
#########################

:date: 2014-11-17 20:00
:category: Code
:tags: python, django
:summary: Found that tests on a recent project started breaking for no clear
          reason, and it turned out it was because I'd used ``get`` to retrieve
          values from Contexts.
:scm_path: content/1411-django-contextlist.rst

Background
==========

If you know me, then you know that I'm an avid tester. It could even be argued
that I test too extensively as part of my day-to-day development, but that's a
post for another day.

On a recent project, a particular view started failing with the error::

    AttributeError: 'ContextList' object has no attribute 'get'

I wasn't happy with just changing the tests to work again, so I dug down into
why they started failing.


TL;DR
=====

To get a value from a Context object returned  by the Django Test Client, then
it's better to use the ``[]`` operator than the ``get`` method.

For example:

.. code-block:: python

    # In a test, after doing
    response = self.client.get(reverse('home'))

    # ... then it's better to use [] to test the context
    self.assertEqual(response.context['name'], 'Homer')

    # ...than to use get
    self.assertEqual(response.context.get('name'), 'Homer')


Reason
======

It turns out that the problem was to do with a developer on the project
changing how the template for the view was generated. They changed a view that
was using a single template, to a couple of templates using `Django's template
inheritance
<https://docs.djangoproject.com/en/1.7/topics/templates/#template-inheritance>`_
and the ``extends`` template tag.

This then effects how Django's test client returns the Context object for
inspection.

To test this I prepared the following test:

.. code-block:: python

    from django.core.urlresolvers import reverse
    from django.test import TestCase


    class Tests(TestCase):
 
        def test_get(self):
            response = self.client.get(reverse('home'))
            self.assertEqual(response.context.get('name'), 'Homer')

        def test_operator(self):
            response = self.client.get(reverse('home'))
            self.assertEqual(response.context['name'], 'Homer')

The home view was just a simple template renderer:

.. code-block:: python

    from django.shortcuts import render


    def home(request):
        return render(request, 'home.html', {'name': 'Homer', })

Simple works
------------

When the 'home.html' template is a simple template with no inheritance (it can
be completely empty), then both tests pass.

'home.html' template code:

.. code-block:: html

    <p>Hello World</p>

Test run:

.. code-block:: sh

    ./manage.py test
    Creating test database for alias 'default'...
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.027s

    OK
    Destroying test database for alias 'default'...


Template inheritance fails with `get`
-------------------------------------

Now adjust 'home.html' to extend another template 'base.html' which has
arbitrary contents.

New 'home.html' template code:

.. code-block:: html

    {% extends 'base.html' %}
    <p>Hello World</p>

Test run:

.. code-block:: sh

    ./manage.py test
    Creating test database for alias 'default'...
    E.
    ======================================================================
    ERROR: test_get (mini.tests.Tests)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/james/active/mini/mmm/mini/tests.py", line 9, in test_get
          self.assertEqual(response.context.get('name'), 'Homer')
    AttributeError: 'ContextList' object has no attribute 'get'

    ----------------------------------------------------------------------
    Ran 2 tests in 0.029s

    FAILED (errors=1)
    Destroying test database for alias 'default'...

So the ``test_get`` case, which was using ``get`` failed.

Conclusion
==========

It's definitely more robust to be using list access ``[]`` on Context objects
returned by the Django Test Client where possible when checking values passed
through to templating.


Grab me on `Twitter <https://twitter.com/jamesfublo/>`_ to discuss testing.

Thanks for reading.
