The benefits of extracting Python packages from projects
========================================================

:date: 2018-04-14 22:00
:tags: language:python
:category: Code
:summary: Thoughts on extracting service code into libraries and the benefits
          that it can bring.
:scm_path: content/1804-pysyncgateway.rst


This week we released version 1 of `pysyncgateway
<https://pypi.org/project/pysyncgateway/>`_ - a Python package for
communicating with Couchbase's Sync Gateway via its REST API.

But this library was not created from scratch - it was created mainly with code
extracted from my employer's Django-DRF-powered server repository. Where I've
extracted this code into the new library, I've been able to shrink the server
code and clean it up. I've thought that this process has been really helpful
and so I thought I'd put together this list of some of the benefits that I've
found so far.


Better separation of concerns
-----------------------------

The boundary between the new library and the server code makes it much easier
to reason about where the responsibilities of each part of the code start and
end.

Originally the Sync Gateway code was tightly knitted with our Django API
server:

* It used Django settings for establishing URLs of the Sync Gateway instance in
  test and production.

* It provided test cases to our server's old ``Unittest`` test suite, Those
  test cases created test Databases, Users and Documents on the Sync Gateway
  for each test - tearing them down afterwards.

* It manipulated the statistical data retrieved from Sync Gateway and posted it
  to our ``statsd`` instance, again the location of which was configured in
  Django settings.

In extracting the library, these responsibilities have been cleaned out and
clarified.

* Communication with Sync Gateway's API from Python - Responsibility of
  ``pysyncgateway``.

* Testing and mitigating any strange behaviours of the Sync Gateway API -
  Responsibility of ``pysyncgateway``.

* Integration of Sync Gateway's objects (User, Document, Database) into
  the API server and Django - Responsibility of API server code.

* Synchronisation of Django's User object with Sync Gateway's User objects -
  Responsibility of API server.
  
This split means that when I've had questions about how Sync Gateway behaves in
certain situations and I need to write a test to explore that, then the
location for that test is clear - it goes in the Sync Gateway library.

This boundary has given me the "space" to write simple failing tests and learn
more about Sync Gateway than I think I ever did when we had one blob of code in
the API server repository.


Improved efficiency of development and test
-------------------------------------------

Efficiency of service layer existing in a separate library. Testing is much
more efficient. A build on `Circle CI
<https://circleci.com/gh/constructpm/pysyncgateway/tree/master>`_ takes around
10s whereas in our API server test suite it was taking 40s.


Tox is great for testing packages
---------------------------------

`Tox <https://tox.readthedocs.io/en/latest/>`_ is a fantastic tool and it comes
into its own when you are creating a package. When I found I'd broken
installation of ``pysyncgateway`` by missing a dependency from the ``setup.py``
``install_requires`` list, I created a special install test environment in ``tox.ini``.

It installs the package with `no other requirements present
<https://github.com/constructpm/pysyncgateway/blob/8e287e4271fcbb61886de11cdd0819b46e595ab1/tox.ini#L12>`_
and gave me added confidence that I'd captured the install requirements
correctly.


Lint and document all the things
--------------------------------

It's very easy to break documentation but having an RST linter really helps.
I've added a step to the code linting which uses `restructuredtext-lint
<https://pypi.python.org/pypi/restructuredtext_lint>`_ to ensure that all RST
is valid - this means that it's much more likely that Github and Read The Docs
will render it as expected. 

Even though the code has been in beta and the API server is (probably) the
only production system using it right now, writing a Changelog really helped
me to clarify what changes I was making to the library.

In general, the built documentation is great. Many of the docstrings were in
place in much of the code, but reading them on the `Read The Docs site
<https://pysyncgateway.readthedocs.io/>`_ or from a local HTML render is really
helpful - I've found it much better than reading docs via a code editor or
``ipython``.


Still a monolith, but with packaging benefits
---------------------------------------------

Our server code remains a single monolith - it's one installed blob of code on
one server. The Sync Gateway code was extracted into a library, not a service.

However, now that the Sync Gateway code is installed from PyPi via
``pip-sync``, there is an additional abstraction that we can select the version
of the library that will be installed.

This means that we have more flexibility to move the library forward to work
with the latest version of Sync Gateway 2 (it's currently only tested with 1.5)
and also Python 3. We can upgrade the library and bump versions without
touching the server monolith at all.
