Building a custom Unittest skip decorator with TDD
==================================================

Reverse engineer the skip test
------------------------------

* The ``FakeTestCase`` is defined inline because its attributes are changed by
  the decorator and it's easier to burn it at the end of the test than to clean
  it up at the end of the test.

.. code-block:: python

    def fake_t_fn():
        """A fake test function"""


    class TestSkip(unittest.TestCase):

        def test_happy_fn_wrap(self):
            """
            Skip wraps a function and preserves its docstring
            """
            result = unittest.skip('__REASON__')(fake_t_fn)

            self.assertEqual(result.__doc__, 'A fake test function')

        def test_happy_fn_exec(self):
            """
            Skip makes skip on a function

            Test function is skipped because it raises SkipTest exception.
            """
            wrapped_fn = unittest.skip('__REASON__')(fake_t_fn)

            with self.assertRaises(unittest.SkipTest) as context:
                wrapped_fn()

            self.assertEqual(context.exception.args[0], '__REASON__')

        def test_happy_cls(self):
            """
            Skip makes skip on a class

            Class is skipped because internal arguments are added which Unittest
            checks for.
            """
            FakeTestCase = type('FakeTestCase', (), {})

            result = unittest.skip('__REASON__')(FakeTestCase)

            self.assertIs(result.__unittest_skip__, True)
            self.assertEqual(result.__unittest_skip_why__, '__REASON__')
            self.assertEqual(result, FakeTestCase)


1. Wrapping
-----------

First test - ensure that our decorator can wrap the function or class and
preserve its docstring.

* Test

.. code-block:: python

    def test_happy_fn_wrap(self):
        """
        skipIntegration wraps a function and preserves its docstring
        """
        result = skipIntegration(fake_t_fn)

        self.assertEqual(result.__doc__, 'A fake test function')

    def test_happy_cls_wrap(self):
        """
        skipIntegration wraps a class and preserves its docstring
        """
        FakeTestCase = type('FakeTestCase', (), {'__doc__': 'Fake test suite'})

        result = skipIntegration(FakeTestCase)

        self.assertEqual(result, FakeTestCase)
        self.assertEqual(result.__doc__, 'Fake test suite')

**NOTE** This test probably fails on the pass-through.

* Code

.. code-block:: python

    def skipIntegration(test_item):
        """
        Skip integration tests if TEST_INTEGRATION setting is set to True.
        """
        return test_item


2. Skip function on ``False``
-----------------------------

Get it to skip when setting is set to ``False``. This uses "fake it 'till you
make it" by not inspecting the setting, but skipping all the wrapped tests.

* Test

.. code-block:: python

    @override_settings(TEST_INTEGRATION=False)
    def test_happy_exec_false(self):
        """
        skipIntegration skips test if TEST_INTEGRATION is false

        Test function is skipped because it raises SkipTest exception.
        """
        wrapped_fn = skipIntegration(fake_t_fn)

        with self.assertRaises(unittest.SkipTest) as context:
            wrapped_fn()

        self.assertEqual(context.exception.args[0], 'Integration tests turned off')

* Code

.. code-block:: python

    def skipIntegration(test_item):
        """
        Skip integration tests if TEST_INTEGRATION setting is True.
        """
        @functools.wraps(test_item)
        def decorator(*args, **kwargs):
            raise unittest.SkipTest('Integration tests turned off')

        return decorator


3. Run function on ``True``
---------------------------

Ensure that if the setting is set, then the test is run. For this it would be
helpful to be able to test the result of the test function to assert that it
ran - so let's adjust that.

.. code-block:: python

    def fake_t_fn(self):
        """A fake test function"""
        return self

This has the added benefit of assuring that a single ``*arg`` can be passed
through.

* Test

.. code-block:: python

    @override_settings(TEST_INTEGRATION=True)
    def test_happy_exec_true(self):
        """
        skipIntegration runs test if TEST_INTEGRATION is true
        """
        wrapped_fn = skipIntegration(fake_t_fn)

        result = wrapped_fn('__ARG__')

        self.assertEqual(result, '__ARG__')

* Code

.. code-block:: python

    def skipIntegration(test_item):
        """
        Skip integration tests if TEST_INTEGRATION setting is True.
        """
        @functools.wraps(test_item)
        def decorator(*args, **kwargs):
            if settings.TEST_INTEGRATION:
                return test_item(*args, **kwargs)
            raise unittest.SkipTest('Integration tests turned off')

        return decorator

4. Test function will be skipped with no setting
------------------------------------------------

* Test

.. code-block:: python

    @override_settings()
    def test_happy_exec_no_setting(self):
        """
        skipIntegration skips if there is no TEST_INTEGRATION setting

        Trusts:
            test_happy_exec_false: Exception message is as expected.
        """
        del settings.TEST_INTEGRATION
        wrapped_fn = skipIntegration(fake_t_fn)

        with self.assertRaises(unittest.SkipTest):
            wrapped_fn()

* Code

.. code-block:: python

    def skipIntegration(test_item):
        """
        Skip integration tests if TEST_INTEGRATION setting is True.
        """
        @functools.wraps(test_item)
        def decorator(*args, **kwargs):
            try:
                if settings.TEST_INTEGRATION:
                    return test_item(*args, **kwargs)
            except AttributeError:
                pass
            raise unittest.SkipTest('Integration tests turned off')

    return decorator

OK. So the function version is completed according to the tests.

Now for the classes...

5.  Do nothing to class on ``True``
-----------------------------------

NOTE: had to do some big refactoring here - not sure how that fits in. The
extraction of 'reason' should be left to a sub-part.

* Test

.. code-block:: python

    @override_settings(TEST_INTEGRATION=True)
    def test_wrap_true(self):
        """
        skipIntegration passes through class if TEST_INTEGRATION is True
        """
        FakeTestCase = type('FakeTestCase', (), {})

        result = skipIntegration(FakeTestCase)

        self.assertEqual(result, FakeTestCase)
        self.assertFalse(hasattr(result, '__unittest_skip__'))
        self.assertFalse(hasattr(result, '__unittest_skip_why__'))

* Code

.. code-block:: python

    def skipIntegration(test_item):
        """
        Skip integration tests if TEST_INTEGRATION setting is True.
        """
        reason = 'Integration tests turned off'

        if isinstance(test_item, type):
            return test_item

        @functools.wraps(test_item)
        def decorator(*args, **kwargs):
            try:
                if settings.TEST_INTEGRATION:
                    return test_item(*args, **kwargs)
            except AttributeError:
                pass
            raise unittest.SkipTest(reason)
        return decorator


6.  Skip class on ``False``
---------------------------

* Test

.. code-block:: python

        @override_settings(TEST_INTEGRATION=False)
        def test_wrap_false(self):
            """
            skipIntegration marks class for skipping if TEST_INTEGRATION is False

            Class is skipped because internal arguments are added which Unittest
            checks for.
            """
            FakeTestCase = type('FakeTestCase', (), {})

            result = skipIntegration(FakeTestCase)

            self.assertEqual(result, FakeTestCase)
            self.assertIs(result.__unittest_skip__, True)
            self.assertEqual(result.__unittest_skip_why__, 'Integration tests turned off')

* Code

.. code-block:: python

    def skipIntegration(test_item):
        """
        Skip integration tests if TEST_INTEGRATION setting is True.
        """
        reason = 'Integration tests turned off'

        if isinstance(test_item, type):
            if settings.TEST_INTEGRATION:
                return test_item
            test_item.__unittest_skip__ = True
            test_item.__unittest_skip_why__ = reason
            return test_item

        @functools.wraps(test_item)
        def decorator(*args, **kwargs):
            try:
                if settings.TEST_INTEGRATION:
                    return test_item(*args, **kwargs)
            except AttributeError:
                pass
            raise unittest.SkipTest(reason)
        return decorator

7.  Skip class on missing
-------------------------

* Test

.. code-block:: python

    @override_settings()
    def test_wrap_missing(self):
        """
        skipIntegration marks class if there is no TEST_INTEGRATION setting

        Trusts:
            test_wrap_false: Correct message was set.
        """
        del settings.TEST_INTEGRATION
        FakeTestCase = type('FakeTestCase', (), {})

        result = skipIntegration(FakeTestCase)

        self.assertEqual(result, FakeTestCase)
        self.assertIs(result.__unittest_skip__, True)

* Code

.. code-block:: python

    def skipIntegration(test_item):
        """
        Skip integration tests if TEST_INTEGRATION setting is True.
        """
        reason = 'Integration tests turned off'

        if isinstance(test_item, type):
            try:
                if settings.TEST_INTEGRATION:
                    return test_item
            except AttributeError:
                pass
            test_item.__unittest_skip__ = True
            test_item.__unittest_skip_why__ = reason
            return test_item

        @functools.wraps(test_item)
        def decorator(*args, **kwargs):
            try:
                if settings.TEST_INTEGRATION:
                    return test_item(*args, **kwargs)
            except AttributeError:
                pass
            raise unittest.SkipTest(reason)
        return decorator

8. refactor
-----------

