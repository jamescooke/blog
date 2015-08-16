Irregular Vim
=============

:date: 2015-08-16 21:00
:tags: vim
:category: Talks
:summary: At July's Vim London I gave a talk about some of Vim's irregular
          behaviours. Using bare-bones Vim to present and demonstrate from is a
          risky business!
:scm_path: content/1508-irregular-vim.rst

My frustrations with Vim arise when it makes actions that are unexpected. At
`Vim London <http://www.meetup.com/Vim-London/events/223784891/>`_ I presented
some of my "pet misbehaviours" - these are the ones that affect my regular use
of Vim.

Background
----------

If you're new to Vim then one of the key features of Vim is that it's a modal
editor. As a result, to quote a quote from a `previous talk
</vi-nature-everywhere-lightning-talk.html>`_:

    The "Zen" of vi is that you're speaking a language.

So what happens when a language has many irregularities and frequently broken
rules? They become hard to learn. For example the `English language is hard
<https://www.oxford-royale.co.uk/articles/learning-english-hard.html>`_
because:

    ... although there are rules, there are lots of exceptions to those rules.

My fear is that if Vim is hard to learn it will be overlooked by new users and
it will cease to exist in the future. I think we should all be working on the
maxim that Drew has put on the `Vim London meetup page
<http://www.meetup.com/Vim-London/>`_:

    Use Vim better, make Vim better.

Pet misbehaviours
-----------------

Here are the five behaviours looked at in this talk, each one linked to its
section in the slides on Github.

- `Linewise motions always include the start and end position
  <https://github.com/jamescooke/irregular-vim-slides/blob/master/10a_motion_exceptions.rst>`_

  **Except** when the end of the motion is in column 1.

- `Change is equivalent to Delete Insert
  <https://github.com/jamescooke/irregular-vim-slides/blob/master/15a_change_is_delete_insert.rst>`_

  **Except** when motion is ``w``.

- `Pasting from registers is easily repeatable
  <https://github.com/jamescooke/irregular-vim-slides/blob/master/20a_pasting_and_registers.rst>`_

  **Except** when in visual modes.

- `Incrementing number after cursor is predictable
  <https://github.com/jamescooke/irregular-vim-slides/blob/master/25a_add_number.rst>`_

  **Except** when the number starts with a ``0``.

- `CTRL-O goes back to old cursor position
  <https://github.com/jamescooke/irregular-vim-slides/blob/master/30a_ctrl_o_goes_jump_older.rst>`_

  **Except** when in visual modes.

Testing process
---------------

Automated and predictable testing is an important part of how I work and so I
attempted to use a repeatable process for testing each of the behaviours.

1. Outline the **assumption** about Vim. Highlight the docs (where available)
   that make the statement or assertion.

2. Do some small **tests** of this assertion. Does it work as expected? How do
   we feel about the behaviour?

3. Update the assertion with any **exceptions** and look at any reasons for
   those exceptions.

Content
-------

`Video on vimeo <https://vimeo.com/135055397>`_ (thanks `Drew
<https://twitter.com/nelstrom>`_).

.. raw:: html

  <iframe src="//player.vimeo.com/video/135055397" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

`Slides are on GitHub <https://github.com/jamescooke/irregular-vim-slides>`_.

Learnings
---------

One of my annoyances that started this journey arose when attempting to delete
everything up to but not including a character. As you'll see at the end of the
talk, I learned a new movement command ``t`` (thanks Audience!).

``t`` is like ``d`` but not inclusive. From the help ``:help t`` file:

    Till before [count]'th occurrence of {char} to the right. The cursor is
    placed on the character left of {char} inclusive. {char} can be entered
    like with the f command.

This exactly solves the problem that started my exploration of Vim's
irregularities. It's a humbling experience when you talk for 20 minutes about
Vim commands and still learn a 'basic' one at the end of the talk. I think that
this is a reminder to me that Vim is deep.

Future
------

I would like to improve these misbehaviours and make them more regular. My hope
is that, if this could be achieved, it would make Vim's interface even more
great and also easier to learn.

The main thing for me going forwards is to use `Neovim <http://neovim.io/>`_. A
project that is open to improving how Vim works. Here's a great post about `why
Neovim is better than Vim
<http://geoff.greer.fm/2015/01/15/why-neovim-is-better-than-vim/>`_ - thanks
`Geoff <https://twitter.com/ggreer>`_.

From there I will check out how many of these irregularities can be improved
with code changes because having to have a ``vimrc`` file that resets Vim to
'regular' behaviour by turning off things like octal numerical increments seems
horrible and repellent to new users.

We can do better.

Thanks
------

- `Drew <https://twitter.com/nelstrom>`_ for asking me to talk and providing
  the ``cw`` example.

- `Kris <https://twitter.com/krisajenkins>`_ for inspiring me at my first Vim
  London meetup with `Barebones Vim navigation <https://vimeo.com/65250028>`_.
  This showed me so much about Vim that I didn't know and also that you **can**
  do a high quality presentation from Vim. (I hope that one day I'll be able to
  meet your standard Kris).

And thanks to you for reading! Grab me on `Twitter
<https://twitter.com/jamesfublo/>`_ with any feedback.
