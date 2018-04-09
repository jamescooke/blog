:date: 2017-04-00 00:00
:tags: language:python
:category: Code
:summary: TODO
:scm_path: content/1804-pysyncgateway.rst
:status: draft

On releasing ``pysyncgateway``
==============================

Background
----------

Construct is an iOS and web app for the construction industry. Under the hood it uses Python 2, Django, Couchbase Sync Gateway and various other tech (which are less important for this post).

Over the last month or so, I have been stripping out code that communicated with Sync Gateway from our API server repository.
This has now been extracted into its own library called `pysyncgateway <https://pypi.org/project/pysyncgateway/>`_ and version 1.0
was released this week.

Learnings
---------

* Efficiency of service layer existing in a separate library. Testing is much more efficient. A build on `Circle CI <https://circleci.com/gh/constructpm/pysyncgateway/tree/master>`_ takes around 10s whereas in our API server test suite it was taking 40s.

* Better separation of concerns. Previous Sync Gateway code integrated with our API server was using Django settings, providing test cases in our old Unittest test suite, manipulating retrieved data for statsd - things that have been cleaned out and clarified.

* More separation of concerns:
  - How best to communicate with Sync Gateway's API from Python - responsibility of ``pysyncgateway``.
  - Pinning any strange behaviours on the API - responsibility of ``pysyncgateway``.
  - Integration of Sync Gateway's objects (User, Document, Database) into Construct's API server and Django - responsibility of API server code.
  - Synchronisation of Django's User object with Sync Gateway's User objects - responsibility of API server.
  
  This split means that when I've had questions about how Sync Gateway behaves in certain situations, the location for the test is clear - ``pysyncgateway``. I've found that that clarity has given me the "space" to write simple failing tests and learn more
  about Sync Gateway than I think I ever did when we had one blob of code in the API server repository.

* Documentation is great. Many of the docstrings were in place, but reading them on the `Read The Docs site <https://pysyncgateway.readthedocs.io/>`_ or from a local HTML render is really helpful - I've found it much better than reading docs from a code editor.

* Still a monolith. This is an extraction of code into a library, not a service. The additional abstraction of being able to select a particular version of ``pysyncgateway`` to use in the API server's requirements means much more flexibility when we come to
  work on moving to version 2 of Sync Gateway which is currently in beta. I think it will also help when we want to move to Python 3 (unfortunately Construct started on Python 2).
  
* Even though the code has been in beta and the API server is (probably) the only production system using it right now, writing a Changelog really helped me to clarify what changes I was making to the library, sometimes as I did them, sometimes afterwards.

* `Tox <https://tox.readthedocs.io/en/latest/>`_ is a fantastic tool and it comes into its own when you are creating a package.
  When I found I'd broken installation of ``pysyncgateway`` by missing a dependency from the ``setup.py``
  ``install_requires`` list, I created a special install test environment in ``tox.ini``.
  It installs the package with `no other requirements present <https://github.com/constructpm/pysyncgateway/blob/8e287e4271fcbb61886de11cdd0819b46e595ab1/tox.ini#L12>`_ and gave me added confidence that I'd captured the install
  requirements correctly.
  
* It's very easy to break documentation but having an RST linter really helps. I've added a step to the code linting which uses ``restructuredtext-lint`` to ensure that all RST is valid - this means that it's much more likely that Github and Read The Docs will render it as expected. 
