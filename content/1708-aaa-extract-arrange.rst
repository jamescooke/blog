AAA Part 2: Extracting Arrange code to make fixtures
====================================================

:date: 2017-08-07 00:00
:tags: language:python, topic:testing
:category: Code
:summary: This post explores how to extract arrangement code when working with
          the Arrange Act Assert pattern so that it can be used with certainty
          across the test suite.
:scm_path: content/1708-aaa-extract-arrange.rst


In this post I will describe how code in tests' Arrange blocks can become
over-complicated, break the AAA pattern and benefit from extraction.


Background
----------

* This post is Part 2 of a series on the Arrange Act Assert pattern for Python
  developers. See `Part 1
  </arrange-act-assert-pattern-for-python-developers.html>`_ for an
  introduction to the pattern and outline of its constituent parts.

* When I mention "code extraction" I'm primarily referring to the Extract
  Method [#em]_ of refactoring. `Kent Beck's book "Test Driven Development: By
  Example"
  <http://www.goodreads.com/book/show/387190.Test_Driven_Development>`_ really
  turned me on to the value in eliminating duplicated code between tests and
  between tests and the SUT [#sut]_.

* I'm using `pytest <https://docs.pytest.org/en/latest/>`_ in this example
  which means that fixtures are marked with the ``@pytest.fixture`` decorator.
  If you're using ``unittest`` then you could extract the set up code into the
  ``TestCase.setUp`` method.

* If you can, perform Extract Method while your test suite is GREEN [#green]_.
  This means that you can be more assured that your refactoring has worked
  without errors.

* During my work I often build permission systems that manage access to
  resources such as files, accounts, projects, etc, based on the connection
  between Users and those resources. The example test below is from one of
  those projects. I often use Simpsons and Futurama characters in tests because
  I think it makes it easier to visualise the test conditions when characters
  are used that other programmers may be familiar with already.


The problem
-----------

I've found that this problem, which I call "Complicated Setup", occurs as a test suite grows and
the complexity of the tests on the outside of the code increases.

Tests will often need to combine a number of objects in increasingly complex
states to build the SUT [#sut]_. As a result, additional assertions are
required before the Act block to ensure that the test conditions are correctly
established. The problem with these additional assertions is that
they break the AAA pattern because there should be no assertions in the Arrange
block.

.. code-block:: python

    # Warning - this test does *not* fit the AAA pattern because it has
    # assertions in the Arrange block.

    def test_owner_invite_admin():
        """
        Leela can invite Bender to an additional Project, Fry is notified

        ----------------+---------------+-----------
         Account Role   | Project Role  | Name
        ----------------+---------------+-----------
         Owner          | -             | Leela
         Admin          | -             | Fry
         Viewer         | Admin         | Bender
        ----------------+---------------+-----------
        """
        # LEELA (and account)
        account = AccountFactory(owner__first_name='Leela')
        account_document = AccountDocument(account, default_database)
        account_document.get_or_create()
        leela = account.owner
        new_project = leela.create_project('new_project')
        # FRY
        admin_membership = AccountMembershipFactory(
            account=account,
            permission='AA',
            person__first_name='Fry',
        )
        fry = admin_membership.person
        # BENDER
        project_data = ProjectMembershipFactory(
            account=account,
            person__first_name='Bender',
            role='admin',
        )
        project_couchbase = project_data['project']
        bender = project_data['person']
        # Check
        assert len(bender.accounts) == 1            # <
        assert bender.accounts[0].owner == leela    # < Assertions in Arrange
        assert len(bender.projects) == 1            # <
        assert bender.projects[0] != new_project    # <
        assert len(fry.messages) == 0               # <

        result = leela.new_project.invite(bender)

        assert result is True
        assert len(fry.messages) == 1

Tests on the arrangement of the SUT will often be informed by the tests that are about
to be carried out on it in the Act. Here I want to ensure that Fry is notified with a new
message so it is important that after Arrange Fry has no messages waiting.
But adding these assertions before the Act section means
breaking AAA and this is a smell the test has grown too complex and should be cut
down.

It is possible to use Extract Method to create a fixture that solves this issue
and returns the test to pure AAA pattern. I've used a simplified example to
illustrate how to solve this below. I've imagined a ``SUT`` class that must be
called with some arrangement functions like ``arrange_a``, ``arrange_b``, etc.

.. raw:: html

    <script async class="speakerdeck-embed" data-id="da526efe5fb6445eadb71b7f4b66c2f5" data-ratio="1.82857142857143" src="//speakerdeck.com/assets/embed.js"></script>


If the example does not load for you, you can `view it on speakerdeck
<https://speakerdeck.com/jamescooke/extract-arrangement-code>`_.

Now applying this process to the Futurama account test above I get the
following fixture with its own dedicated test and a much simpler test for the
invite behaviour.

.. code-block:: python

    @pytest.fixture
    def account_members():
        """
        Returns:
            tuple:
                User: Leela - Account owner.
                User: Fry - Admin.
                User: Bender - Project admin.

        ----------------+---------------+-----------
         Account Role   | Project Role  | Name
        ----------------+---------------+-----------
         Owner          | -             | Leela
         Admin          | -             | Fry
         Viewer         | Admin         | Bender
        ----------------+---------------+-----------
        """
        # LEELA (and account)
        account = AccountFactory(owner__first_name='Leela')
        account_document = AccountDocument(account, default_database)
        account_document.get_or_create()
        leela = account.owner
        new_project = leela.create_project('new_project')
        # FRY
        admin_membership = AccountMembershipFactory(
            account=account,
            permission='AA',
            person__first_name='Fry',
        )
        fry = admin_membership.person
        # BENDER
        project_data = ProjectMembershipFactory(
            account=account,
            person__first_name='Bender',
            role='admin',
        )
        project_couchbase = project_data['project']
        bender = project_data['person']
        return leela, fry, bender

    def test_account_members(account_members):
        """
        Fry has no pending messages and Bender is a member of the Account
        """
        result = account_members

        assert len(result) == 3
        leela, fry, bender = result
        assert len(bender.accounts) == 1
        assert bender.accounts[0].owner == leela
        assert len(bender.projects) == 1
        assert bender.projects[0] != new_project
        assert len(fry.messages) == 0

    def test_owner_invite_admin(account_members):
        """
        Leela can invite Bender to an additional Project, Fry is notified
        """
        leela, fry, bender = account_members

        result = leela.new_project.invite(bender)

        assert result is True
        assert len(fry.messages) == 1

Even though this example is long winded, I hope you can see that the
extraction of the set up code into its own fixture has simplified the tests and
brought the code back into conformity with the AAA pattern.


Benefits of extraction
----------------------

The result of the extraction process is a pair of tests with a single fixture. The tests
fit the AAA pattern that I advocated in Part 1 of this series and the resulting
code's structure has a number of advantages for the future of the test suite:

* Continued development on the fixture can happen using TDD [#tdd]_ by adding
  new requirements to ``test_fixture()`` and then expanding the fixture to get
  back to GREEN.

* The resulting fixture can be reused really easily. Permutations of different
  actions on a particular SUT can be easily tested without having to depend on
  our power of copy and paste and without creating more duplicated code.

* If a situation arises in the future where the arrangement of the SUT needs to
  change in the fixture all the tests that use it *might* fail. However, the
  payoff for the additional failure of the fixture's dedicated tests is that
  there is the opportunity to fix the problem in one place - the extracted code
  in the fixture.

  On top of that, the fix can be performed using TDD because the fixture is
  already extracted and under test - a potential double win.

In this way the test suite remains dynamic, clear and able to adapt with the
software it's testing.

Should all fixtures have their own tests?
-----------------------------------------

I'm often asked whether I think test fixtures should be tested. My answer is:
"It depends".

When the fixture was arrived at via "Complicated setup" then my answer is
"yes". As we've seen, the ``test_fixture()`` test remains to pin the fixture's
behaviour and assert that the SUT is in the expected state.

When the fixture has been extracted because of "Setup duplication" [#sd]_ there will
be a fixture created that does not have its own explicit test. Instead, the
fixture is tested implicitly by the two tests but does not have a dedicated
test of its own.

For me this is an "OK" situation and if it turns out that the fixture should be
adjusted then a fixture test can be created to facilitate that change under the
usual RED, GREEN, REFACTOR cycle.


Happy testing!


Tiny glossary
-------------

.. [#em] Extract Method is a refactoring step `defined here
    <https://refactoring.com/catalog/extractMethod.html>`_.

.. [#sut] `System Under Test
    <https://en.wikipedia.org/wiki/System_under_test>`_ I've used this to mean the
    Unit under test, there is no implication around the size of the "system" or
    "unit".

.. [#green] GREEN is the name for the state when all tests in your suite pass.

.. [#tdd] Test Driven Development.

.. [#sd] Setup duplication: My name for the situation where there are large
    chunks of Arrange code duplicated between tests. This topic warrants a
    follow-up post.
