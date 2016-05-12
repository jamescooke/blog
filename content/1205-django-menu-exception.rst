Fixing exception in django-menu
###############################

:date: 2012-05-05 19:40
:tags: topic:django
:category: GitHub Contributions
:summary: A tiny pull request to stop django-menu from throwing exceptions on
          new unconfigured sites.

`django-menu <https://github.com/rossp/django-menu/>`_ is a nice simple library for building very simple menus. However, when a site is loaded for the first time, the menu structure was not configured and so it was throwing a ``DoesNotExist`` Exception.

This tiny `pull request <https://github.com/rossp/django-menu/pull/5>`_ simply
wrapped the call to the menu in a ``try``/``except`` so that new sites using
django-menu won't fall over on first load.
