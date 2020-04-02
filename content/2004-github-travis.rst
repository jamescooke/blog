Travis hitting GitHub's API limits for Open Source projects
===========================================================

:date: 2020-04-02 18:00
:tags: topic:testing
:category: Code
:summary: GitHub's API rate limits.
:scm_path: content/2004-github-travis.rst

Last week, GitHub's Dependabot created `a pull request
<https://github.com/jamescooke/flake8-aaa/pull/138>`_ with a fix to a
vulnerability found the development dependencies of one of my FOSS projects.
This was a bump to Mozilla's `bleach <https://github.com/mozilla/bleach>`_, a
project that GitHub states is used by more than 61,000 other projects.

.. image:: |filename| images/200402_pr.png
    :alt: GitHub's Dependabot opened a PR to bump bleach in Flake8-AAA.
    :target: https://github.com/jamescooke/flake8-aaa/pull/138

`Flake8-AAA's repository <https://github.com/jamescooke/flake8-aaa>`_ is wired
into Travis CI to provide automated execution of its test suites across all
supported versions of Python. Better still, because Flake8-AAA is an open
source public repository, Travis provides the computing power to run these
tests for free. I've always found Travis to be reliable and stable as a CI
system - and therefore made a "green" passing Travis build a requirement for a
PR to be merged into Flake8-AAA's master branch.

Unreported build status
-----------------------

However, when I checked on the Dependabot Pull Request, GitHub was still
waiting for the status of its Travis build to be reported.

.. image:: |filename|/images/200401_some_checks_havent_completed_yet.png
    :alt: GitHub's merge dialogue box showing that expected tests have not
        completed.

You can see that the "Merge pull request" box is greyed out because the
required Travis build has not completed yet according to GitHub.

**But** here's the build at `Travis
<https://travis-ci.org/github/jamescooke/flake8-aaa/builds/669024353>`_ - both
green *and* done within 3 minutes of Dependabot opening the PR at GitHub:

.. image:: |filename|/images/200402_green_build.png
    :alt: Travis build of the Dependabot PR is green.

So the call from Travis to GitHub to report the build status on the commit
failed for some reason.

Debugging
---------

Sometimes webhook and API calls to GitHub fail - I've seen this with both
personal and work projects. Often the simplest solution is to retrigger the
build in some way. At first I tried to get a follow up build to work by:

* Creating a new commit on the branch with updated requirements and pushing
  that to the branch.

* Amending the existing commit and pushing with ``--force``.

* Creating and pushing a new branch with an update to all requirements.

All of these strategies had the same effect - a new build was triggered on
Travis and that build was green, but it was not reported to GitHub. So it
looked like all API calls were failing from Travis to GitHub.

Next, while checking the `GitHub status page <https://www.githubstatus.com/>`_
and `Travis status page <https://www.traviscistatus.com/>`_, I found this
status update on the Travis site:

.. image:: |filename| images/200402_travis_status.png
    :alt: Travis status page shows GitHub commit status issue: GitHub status
        may not be posted on commits occasionally from builds using the legacy
        Services integration.
    :target: https://www.traviscistatus.com/incidents/rx6fhs3wqcln

In light of that status message, I tried installing the Travis app integration,
but had no success getting it to link to Flake8-AAA.

The message says:

    Please write to support@travis-ci.com if you encounter any similar
    problems.

So I emailed.

Reply from Travis Support
-------------------------

Here's the full text of the reply from Travis support:

    MK (Travis CI)

    Mar 31, 15:38 EDT

    Hello ,

    Thanks for your patience on this issue.

    We want to provide some visibility into the issues we are facing, the
    effects on our infrastructure and efforts made so far to restore normalcy.

    1. We recently started hitting API rate limits for Github calls and on
       March 25, 2020, we contacted Github to ask for increases and are
       awaiting their feedback in this regard.

    2. On the Travis CI end, we have made improvements on how our code accesses
       the Github API, which has led to improvements, albeit minimal.

    3. While we occasionally hit API limits, it's important to note that we
       haven't hit these kinds of limits before now. In the interim, the
       best course of action would be to retry the action you wanted to
       perform.

    For next steps,

    1. We are following up with Github via various channels to get the
       requested API rate limit increased.

    2. In addition, we are looking for more avenues to remove
       invalid/unnecessary Github API calls in our codebase to ensure we stay
       under the limit and avoid disruptions like this.

    3. We are coordinating internally to ensure customers are up-to-date on
       progress made so far.

    We know how critical our platform is to your business and our goal is to
    provide the best experience for our customers. In line with this, we extend
    our sincere apologies for inconveniences this is causing.

    Thank you and we will provide periodic updates as we have more.


