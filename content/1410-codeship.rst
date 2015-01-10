Current state of Codeship
#########################

:date: 2014-10-12 18:00
:category: Testing
:summary: For the last month I've been using Codeship for Continuous
          Integration on my current client project. These are my current
          thoughts on this hosted service that works with Github and BitBucket
          repositories.
:scm_path: content/1410-codeship.rst

Background
==========

In September I was introduced to `Codeship <https://www.codeship.io/>`_ at a
presentation by `Paul Love <http://anglepoised.com/>`_.  These are some of the
learnings I have from using their hosted service primarily for `Continuous
Integration <http://en.wikipedia.org/wiki/Continuous_integration>`_ for the
last couple of weeks on a client project.

This post isn't about advantages and disadvantages of CI or `Continuous
Delivery <http://en.wikipedia.org/wiki/Continuous_delivery>`_, but more focused
on Codeship's offering currently, compared to other CI services I've used over
the last 6 months or so.

TL;DR
=====

Codeship is relatively new and working hard to stabilise the system while
providing documentation and service.

The 100 free builds they provide per month, along with the ability to integrate
with `BitBucket <https://bitbucket.org/>`_ mean that you can run private
projects on CI for free, but watch out for their lack of stability.

Positives
=========

Good value
----------

Codeship currently offers `100 builds a month for free
<https://www.codeship.io/pricing>`_ on private repos that include BitBucket and
`Github <https://github.com/>`_ - this is **GOOD**. It's hard to find hosted CI
systems that will work with non-Github repository hosting.

Good support
------------

Codeship's support team know their stuff.

I've had multiple discussions with Codeship's support via email and Twitter and
I've found that they get back to you with timely email replies and suggestions
about why things are breaking. Great for a free service!

Good speed
----------

**Builds are QUICK!** So quick that I thought they weren't using a real DB and
wrote a test to prove that they were listening to the settings I'd pushed
specifically for Codeship.

Negatives
=========

Unfortunately the good freeness above comes with some disadvantages.

False negatives
---------------

Some of my builds have received false negatives meaning they have failed when
they shouldn't have. This is annoying but manageable and can often be solved by
re-running the build.

For example, I've had a couple of builds happen on an instance where the
database wasn't available when the tests started running, so everything went
RED. Slack then went RED. Client team start worrying.

Codeship's solution for this was "Add `sleep 3` to make the tests wait 3
seconds before running". This works but why isn't Codeship's instance build
process checking this before starting the run?

False positives
---------------

Builds have received false positives. They have passed when they shouldn't
have - and this is **far worse** than a false negative.

This week a build on Codeship had `git submodule init` fail, but the build
didn't go red. The same condition happened last week and the build *did* fail.
While I'm writing this, Codeship are looking into the problem.

Scarce documentation
--------------------

It's not very clear how to work with teams, amongst other topics. Team members
can't see how many remaining free builds are available each month so they can't
see if they're using up the allowance of free builds quickly or not.

Artefacts need special attention
--------------------------------

It's hard to get build artefacts off Codeship's build instances since the
system burns the instance once the build is complete regardless of result. This
means if you don't push artefacts off the server yourself with a script,
they're gone.

Compare with `CircleCI <https://circleci.com/>`_ - they `keep build artefacts
in a special folder <https://circleci.com/docs/build-artifacts>`_ available for
further processing, downloading, or access after the build is complete.

Test commands are in Codeship not repo
--------------------------------------

A minor gripe I have with the Codeship system is that the test setup and run
commands are stored in the configuration for the project on their site. With
Travis for example, the server runs the commands it finds in ``.travis.yml``.

The benefit of putting the test commands in the repo is that they can be easily
coordinated with git commits - if you want to change how something is run, you
can do it all in the code, commit and push.

The Codeship way means copy-and-pasting run commands up onto their website and
then pushing new code to be tested with those settings. It makes it hard to
prove which branch was run with which settings, or if things were changed to
make builds pass.

Summary
=======

Most concerning are the false negatives and positives on build. It's very
important that a dev team can trust their CI/CD service 100%. These are the
results for the current Django project I'm building on Codeship:

.. raw:: html

    <script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>

.. math::

    \frac {1\ False\ Negative + 1\ False\ Positive}
          {37\ Total\ Builds} = 5\%\ Incorrect\ Results

These are the false builds that I'm aware of - there might be some that have
gone unnoticed. For me, a figure of 95% success makes Codeship 'just' stable
enough for work, but it's **free and works with Bitbucket** and that's a
massive positive. I would be disappointed if we were on a paid account and
receiving the same instability.

For the future, if they can stabilise the builds and document the system then
they could become the go-to CI service for teams on Bitbucket.

Project Background
==================

I'm running 125 tests in around 15s on a Python (2.7) Django (1.7) project that
makes integrated API calls to Dropbox, sits on top of MySQL, runs coverage and
flake8.

Grab me on `Twitter <https://twitter.com/jamesfublo/>`_ to discuss testing and
CI.

Thanks for reading.
