Pyramid London talk - A testing strategy for Pyramid Applications
#################################################################

:date: 2013-06-16 21:00
:tags: pyramid, talk
:summary: Talk at Pyramid London meetup about testing strategies for Pyramid applications.

Pyramid London meetup `returned in June <http://www.meetup.com/The-London-Pyramid-Group/events/119944802/>`_ to `Skills Matter <http://skillsmatter.com>`_. This time I spoke about testing strategies for Pyramid applications.

As outlined in the slides below, my current testing framework builds up with doctests, through unit and integration tests to functional / behaviour driven testing on the outside of the application. Hopefully my very basic "drawn on Google Docs" diagram of the Pyramid Framework illustrates how each of the testing methods fits within the framework.

I would like to have been able to talk more about Behaviour Driven Development and `testing with Behave <http://pythonhosted.org/behave/>`_, which I'm enjoying at the moment, but maybe that's for another presentation. Again, putting together this presentation was really helpful - it helped me to reflect on the methods we're using at the moment, and how I might be able to improve and progress the level of test driven development in my daily work.

.. raw:: html

    <br>
    <script async class="speakerdeck-embed" data-id="57b235d0b8f1013000d27aa19dd2a8cb" data-ratio="1.33333333333333" src="//speakerdeck.com/assets/embed.js"></script>
    <br>

`Video is available via the SkillsMatter site <http://skillsmatter.com/podcast/ajax-ria/pyramid-sqlalchemy-testing-and-auth-policy/mh-7528>`_.

Many thanks to `Armin Ronacher <http://lucumr.pocoo.org/>`_ for his talk on `SQLAlchemy <http://docs.sqlalchemy.org>`_ at the same Pyramid meetup - the `video is also online at SkillsMatter <http://skillsmatter.com/podcast/ajax-ria/pyramid-sqlalchemy-testing-and-auth-policy-4266>`_. As well as the technical details and some hints for things to check out with SQLA, I found Armin's thoughts on how the Pyramid community might improve on how we introduce new developers to Pyramid and SQLAlchemy very helpful. I hope I might be able to contribute to that some time in the future.
Hopefully we'll see more people at the next Pyramid Meetup which may include a talk on using `Celery <http://www.celeryproject.org/>`_ with Pyramid.
