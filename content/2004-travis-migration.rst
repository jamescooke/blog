Migrating Open Source projects on Travis CI to fix GitHub API limit problems
============================================================================

:date: 2020-04-23 23:00
:tags: topic:testing
:category: Code
:summary: Open source maintainers can move their projects from travis-ci.org to
          travis-ci.com to get more reliable GitHub integration.
:scm_path: content/2004-travis-migration.rst

Previously I wrote that `Travis dot org has been exhausting its GitHub API rate
limit </travis-hitting-githubs-api-limits-for-open-source-projects.html>`_.
Test results for projects built on Travis dot org (travis-ci.org) have not
been reliably reported back to GitHub. This leaves commits on GitHub in a
pending yellow status and pull requests blocked.

The solution is for open source maintainers to migrate their projects from
Travis dot org to Travis dot com (travis-ci.com). This solves the API rate
limit problem because Travis dot com uses GitHub Apps, whereas Travis dot org
uses a GitHub integration.

With GitHub Apps `each install of the app gets its own API quota
<https://developer.github.com/apps/differences-between-apps/#token-based-identification>`_.
So with the Travis dot com GitHub app installed in your GitHub user or
organisation, the 5,000 requests per hour API limit applies to just your
install of the app, not globally for all Travis dot com calls to GitHub. As a
small-time open source developer, there are no realistic future scenarios where
my install of the app will reach 5k requests per hour.

Key migration points
--------------------

The `migration documentation on Travis
<https://docs.travis-ci.com/user/migrate/open-source-repository-migration/#migrating-a-repository>`_
is pretty comprehensive, but watch out for these gotchas:

* Make sure you "Sign up for the beta" of migration in `your Travis dot org
  account <https://travis-ci.org/account/repositories>`_.

  .. image:: |filename| images/200424_travis_sign_up.png
      :alt: Travis "Sign up for beta" call to action

  Without this your existing repositories will not appear in your new Travis
  dot com account.

* If you have required checks in the branch protection rules of your GitHub
  project repository, these need to be switched over.

  .. image:: |filename| images/200424_branch_status_checks.png
      :alt: GitHub branch status checks required

  You will need to trigger a build on Travis dot com for these new checks to
  appear as options.

* Remember to change any build badges on your README from dot org to dot com.

A trade off
-----------

With GitHub apps, results of checks are kept in the Checks Framework. This
means that when you click "details" of a Travis dot com check, you will be
shown GitHub's page for this check (`here's an example
<https://github.com/jamescooke/flake8-aaa/pull/140/checks?check_run_id=582544560>`_).
Whereas with Travis dot org, clicking on the "details" link for a check took
you straight to Travis dot org.

Here's how GitHub advertises this benefit:

.. image:: |filename| images/200424_travis_checks_integration.png
    :alt: Integrations built with Checks API - Travis CI - Get a complete
        picture of a project’s health directly from GitHub by viewing your
        build's stages, jobs, and results, including the config associated with
        them. You can also re-run builds from within the GitHub interface.  

Once you migrate your project, Travis will be one click further away. Therefore
you are more likely to stay on GitHub while nursing a pull request or checking
on a build.

While I'm sure many people consider this an improvement, I'm not a fan of the
GitHub checks system. I prefer the old system because:

* It was easier and more reliable to visit the external build system's site. As
  we've seen with this whole issue, communication across GitHub's boundary can
  be unreliable.

* I prefer Travis's interface for showing build information, not GitHub's
  static checks page.

Finally
-------

Thanks to MK at Travis for the help with migration.

I'm glad that it was possible to find a way to continue to use Travis on my
open source projects.

Happy building!
