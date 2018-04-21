Packaging checklist
===================

:date: 2018-05-21 19:00
:tags: language:python
:category: Code
:summary: Pack your Python bags before you ship to PyPI land.
:scm_path: content/1805-packaging-checklist.rst
:status: draft

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


Lint
----

It's very easy to break documentation but having an RST linter really helps.
I've added a step to the code linting which uses `restructuredtext-lint
<https://pypi.python.org/pypi/restructuredtext_lint>`_ to ensure that all RST
is valid - this means that it's much more likely that Github and Read The Docs
will render it as expected. 

Even though the code has been in beta and the API server is (probably) the
only production system using it right now, writing a Changelog really helped
me to clarify what changes I was making to the library.
