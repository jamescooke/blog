Django-mailchimp compatability with v1.3 API
############################################

:date: 2012-09-25 07:14
:tags: django, mailchimp
:category: GitHub Contributions
:summary: Some small updates to the django-mailchimp library to upgrade to the latest Mailchimp API.

For a `Fublo </pages/fublo-ltd.html>`_ project with `Neuxpower
<http://www.neuxpower.com/>`_, we had to communicate with `Mailchimp via their
API <http://apidocs.mailchimp.com/>`_. On Django one of the best libraries for
this is `django-mailchimp <https://github.com/piquadrat/django-mailchimp>`_.

However, in its previous state django-mailchimp wasn't able to specify a ``send_welcome`` parameter which lets Mailchimp know whether it should send out a list welcome message when a new user subscribes. For the project, we were managing the signup explicitly with Neuxpower's code, so no welcome message was required and the default for Mailchimp was ``True`` for sending meaning that Neuxpower's new customers would get hit with a double welcome message... Not desirable.

This `small change <https://github.com/piquadrat/django-mailchimp/pull/6>`_ is now merged in with the library, which has rolled up to a 'v1.3' status as there is no backward compatibilty.
