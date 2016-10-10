Django Factory Audit
====================

:date: 2016-10-12 10:00
:tags: language:python, topic:testing, topic:django
:category: Code
:summary: Exploring the various model instance factories available for Django.
          Each factory is tested based on the quality of the instances it
          creates. Bonus: talk version and slides also available.
:scm_path: content/1610-factory-audit.rst

Factories build instances, primarily for testing, but can be used anywhere.

I'm a bad programmer. I make mistakes, forget to validate my instances, and I'd
like whatever object factory that I use to look after me by validating the
generated instance before it reaches the database.

The Problem
-----------

This is the way that I've been looking at Django model instances - for a single
model we can imagine sets of instances which might look like:

VENN DIAGRAM

Where:

* ``ε``: The universal set of all possible instances of this model.

* ``D``: The set of instances that the database would consider valid. It's
  interesting to note that this set might change as code is developed, tested
  and run on machines that have different database versions or use different
  databases altogether.

* ``V``: The set of valid instances which pass ``full_clean``.

The main issue is the set ``D/V`` of instances. These are all the instances
which can be saved into the database but are considered invalid by Django. When
factories create instances that reside in this set, they create instability in
the system:

* If a user attempts to edit that instance through the Django Admin system,
  then they may not be able to save their changes without fixing a list of
  invalid fields.

* Test suites will be execute using model instances that *should* not be
  created during the "normal" lifetime of the application.

We could argue that way in which Django does not call ``full_clean`` before it
writes instances to the database is the root of the problem - I've previously
`written about this <{filename}/1511-django-save-vs-fullclean.rst>`_ and spoken
about it too. However, this is more a "condition of the environment" and
therefore something that we need to manage, rather than fix.

So let's wage war on this ``D/V`` set - the white of the fried egg in the
diagram.

Factory libraries
-----------------

COPY FROM repo WHEN DONE

Test conditions
---------------

The code used to test the factory libraries is available in the `Factory Audit
repository <https://github.com/jamescooke/factory_audit>`_. For each factory
library, two factories have been created in the default state to create and
save instances of:

* ``ItemFactory``: to create and save instances of ``plant.models.Item``, a
  test model defined `in the 'plant' app
  <https://github.com/jamescooke/factory_audit/blob/master/factory_audit/plant/models.py>`_.

  .. code-block:: python

      class Item(models.Model):
          """
          Single Item with one required field 'name'
          """
          name = models.CharField(max_length=1, unique=True)

  This example has been taken from the `Factory_Djoy README
  <https://github.com/jamescooke/factory_audit>`_ but with a reduced length of
  name down to one character to more easily force name collisions.

* ``UserFactory``: to create and save instances of the default
  ``django.contrib.auth`` User Model.

The goal is that each factory should generate 10 valid instances of each model.

Gradings
--------

Each factory library has been graded based on how its default configuration
behaves when used with the ``Item`` and ``User`` models.

The gradings are based on the definition of "valid". Valid instances are ones
which will pass Django's ``full_clean`` and not raise a ``ValidationError``.
For example, using the ``ItemFactory`` a generated item passes validation with:

.. code-block:: python

    item = ItemFactory()
    item.full_clean()

The gradings are:

- \:red_circle: RED - Factory creates **invalid** instances of the model and
  saves them to the database.

- \:yellow_heart: YELLOW - Factory raises an exception and does not save any
  instances. Preferably this would be a ``ValidationError``, but I've also
  allowed ``IntegrityError`` here.

- \:green_heart: GREEN - Factory creates multiple **valid** instances with no
  invalid instances created or skipped. Running factory ``n`` times generates
  ``n`` valid instances.

The tests on each of the factories have been written to pass when the factory
behaves to the expected grade. For example, the test on Factory Djoy's
``ItemFactory`` expect that it raises ``ValidationError`` each time it's used
and `is therefore YELLOW grade
<https://github.com/jamescooke/factory_audit/blob/master/factory_audit/plant/tests/test_factory_djoy_factories.py#L12-L20>`_.
