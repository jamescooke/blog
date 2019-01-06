Flake8-AAA 0.6 Dev Log
======================

:date: 2019-01-31 19:00
:tags: language:python
:category: Code
:summary: Dev log from my work on version 0.6.0 of the flake8-aaa test linter.
:scm_path: content/1901_flake8_aaa_dev_log.rst
:status: draft

Line-wise versus node-wise analysis and footprints
--------------------------------------------------

As of this new version the analysis of spacing is now fully moved over to a
line based analysis. The general strategy.

Link to 

To help with debugging, I've had the idea that a command line output would be
helpful and I've finally got it in place. This was a great help for checking on
the generation of footprints.


Act Blocks are not Act Nodes
............................

As a result of new footprinting code, I ran into a bug where `footprinting
failed when the Act Block is inside a context manager
<https://github.com/jamescooke/flake8-aaa/issues/60>`_. This often happens when
mocks are deployed using the ``with mock.patch()`` structure.

As a result of this, I've had the realisation that what I've so far defined as
an Act Block is really a smaller thing - an Act Node.


Writing up strategy
...................

Mypy is good, but 

Github projects are odd
.......................

In order to capture the bunch of work around how spacing between blocks was
checked, I tried out Github's Projects tab and created an `Improve analysis of
spacing <https://github.com/jamescooke/flake8-aaa/projects/1>`_ project. For me
on this small project with very low volume, I found it overkill compared to
Issue Timelines. I completely understand that development tools need to be
customisable - and there's probably some great uses for larger projects, but
this didn't work for me this time.


Next to do
----------

These are the items that I'm thinking about, but haven't created tickets for.

noqa
....

I'm pretty sure that many of the rules built so far can not be properly ignored
by the use of the ``# noqa`` comment marker at the end of the offending line.
My plan is to build out a set of tests in the `examples folder
<https://github.com/jamescooke/flake8-aaa/tree/master/examples>`_ called
"ignores". These will have failing examples for each rule, but with ``# noqa``
appended to each so that testing passes.
