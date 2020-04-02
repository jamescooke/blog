Travis hitting GitHub's API limits for Open Source projects
===========================================================

:date: 2020-04-02 23:00
:tags: topic:testing
:category: Code
:summary: GitHub's API rate limits are hurting Travis CI's service quality.
    What does this mean for the future of the GitHub ecosystem?
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
tests for free. I've always found Travis reliable and stable, so it's a
requirement that pull requests have a "green" Travis build before merging into
Flake8-AAA's master branch.

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
green *and* done within 3 minutes of Dependabot opening the PR at GitHub, so
the call from Travis to GitHub to report the build status on the commit failed
for some reason.


.. image:: |filename|/images/200402_green_build.png
    :alt: Travis build of the Dependabot PR is green.


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

Firstly, thanks to Travis support for this helpful message - it's pretty
unusual for a service that offers a free tier to be open and responsive to
messages from freeloading users like myself.

Secondly, I assumed that Travis would not be opposed to publishing the text of
the email since it should help other developers in my situation.

In response to the mail itself:

* My understanding is that this issue mainly affects open source projects on
  Travis dot org.

* This message makes no mention of migrating to the Travis dot com GitHub Apps
  integration, so I assume that it wouldn't work for Flake8-AAA or other open
  source projects.

* The mail states:

      In the interim, the best course of action would be to retry the action
      you wanted to perform.

  Unfortunately I've had no success with this yet, but will continue to try.

Although I'm happy with the Travis response so far, I'm worried about what this
means about the future of GitHub.

Thoughts on the GitHub ecosystem
--------------------------------

I was not part of the "mass exodus" from GitHub in 2018 after `Microsoft
completed its purchase
<https://github.blog/2018-10-26-github-and-microsoft/>`_ of the platform. At
the time I thought that this could only be good for the site, however, now I'm
reconsidering, especially in the light of the situation above. Let me explain
why...  

GitHub wants Actions to replace Travis
......................................

`GitHub Actions <https://github.com/features/actions>`_ is what GitHub calls
its "world-class CI/CD" system. CI/CD has been supported by Actions since
August 2019 and is free for open source projects - GitHub has "embraced" CI/CD.

Travis dot org is now a **competitor** to GitHub rather than the helpful
addition to the ecosystem it was before.

Also the existence of CI/CD in Actions means that GitHub can allow the
degradation of other CI/CD integrations because it's able to offer a "better"
replacement - use Actions instead. My guess would be that GitHub intends
Actions to replace all CI/CD building on GitHub for open source projects.

GitHub wants developers to stay on GitHub
.........................................

In the final paragraph of the `GitHub blog post above
<https://github.blog/2018-10-26-github-and-microsoft/>`_, Nat Friedman states:

    Our vision is to serve every developer on the planet, by being the best
    place to build software.

Building software includes CI/CD and GitHub's vision means that every developer
that needs a CI/CD function would stay on GitHub while "building software", not
traverse external systems like Travis, Circle CI or Codeship.

GitHub can make it harder for CI/CD integrations to keep up
...........................................................

Since GitHub (and therefore Microsoft) `acquired Dependabot in 2019
<https://dependabot.com/blog/hello-github/>`_, GitHub now has a tool which it
can use generate a larger number of builds on CI/CD services integrated with
its platform like Travis. This will have the knock on effect of making it
harder for those CI/CD services to keep within their API rate limits and more
expensive to run because they will need to buy more computing power from AWS
and or Google to run builds.

Best of all for GitHub, they can put this pressure on others while maintaining
the guise of `making "dependency upgrades easy"
<https://github.blog/2019-05-23-introducing-new-ways-to-keep-your-code-secure/#automated-security-fixes-with-dependabot>`_.
Now GitHub automatically creates a pull request for any project owned by an
account with security alerts enabled when it finds a relevant security
vulnerability alert.

In the case of the pull request above that started this post, that was a
vulnerability in bleach. As I mentioned this is a project used by over 60k
projects on GitHub. So when a security advisory on bleach occurs, Dependabot
creates a pull request on GitHub, each pull request will then be built by a
CI/CD system for those repositories that have one wired in. For an external
CI/CD system like Travis, that flood of builds requires a large volume of
computing resources **and** GitHub API calls.

The `GitHub rate limit documentation
<https://developer.github.com/v3/#rate-limiting>`_ currently states a quota of
5,000 requests per hour. If each CI/CD build requires 2 API calls (one to say
"in progress" and one to post the result), then once 2,500 builds are completed
in an hour the quota will be exhausted. If  4% of all the repositories that
depend on bleach are using Travis for builds, then a single bump to the bleach
release would exhaust a 5,000 request quota immediately - and that's before any
"normal" human-driven regular build activity is taken into consideration.

Now I'm pretty sure that Travis has an hourly quota that's greater than 5,000
requests per hour, probably granted to them when GitHub saw them as augmenting
the GitHub ecosystem, but when the Travis email above stated:

    We are following up with Github via various channels to get the requested
    API rate limit increased.

... why would GitHub bump this now?

Instead, GitHub can leave Travis in an awkward situation: choose to throttle
builds and get reliable status calls back to the GitHub API, or make open
source projects have a less reliable and smooth experience when status update
API calls are dropped. Either option makes GitHub Actions look "better" as a
CI/CD solution - a win for GitHub.

Finally, hope
-------------

I hope that my thoughts on the GitHub ecosystem above are overly negative and
that these issues with Travis are not the start of an "extinguish" strategy by
GitHub towards external CI/CD systems (see `Embrace, extend, extinguish
<https://en.wikipedia.org/wiki/Embrace,_extend,_and_extinguish>`_).

I hope I'm completely wrong and that GitHub open up their API limits to Travis
so that open source projects like Flake8-AAA can still use it for reliable
CI/CD. But if things don't go well then I'm certainly more ready to join the
GitHub exodus, just 18 months behind the curve.

Thanks Travis CI for all the builds, I hope we have many more to come!
