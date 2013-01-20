Django-mailchimp compatability with v1.3 API
############################################

:date: 2012-09-25 07:14
:tags: github, python, django, mailchimp
:category: GitHub Contributions

For a fublo project with `Neuxpower <http://www.neuxpower.com/>`_, we had to communicate with `Mailchimp via their API <http://apidocs.mailchimp.com/>`_. On Django one of the best libraries for this is `django-mailchimp <https://github.com/piquadrat/django-mailchimp>`_.

However, in its previous state django-mailchimp wasn't able to specify a ``send_welcome`` parameter which lets Mailchimp know whether it should send out a list welcome message when a new user subscribes. For the project, we were managing the signup explicitly with Neuxpower's code, so no welcome message was required and the default for Mailchimp was ``True`` for sending meaning that Neuxpower's new customers would get hit with a double welcome message... Not desirable.

This small change is now merged in with the library, which has rolled up to a 'v1.3' status as there is no backward compatibilty.

* `GitHub Issue <https://github.com/piquadrat/django-mailchimp/issues/5>`_
* `GitHub Pull Request <https://github.com/piquadrat/django-mailchimp/pull/6>`_
