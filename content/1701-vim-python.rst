My Vim setup for Python development
===================================

:date: 2017-01-04 14:30
:tags: vim
:category: Code
:summary: My current Vim setup for Python development.
:scm_path: content/1701-vim-python.rst

Below is a list of my Vim plug-ins and configurations.

My goal has been to make Vim more useful for (primarily) Python development.
This post refers to Vim 7, because I have not yet updated to Vim 8. I'm using
`vim-plug <https://github.com/junegunn/vim-plug>`_ to manage my packages, so
mentions of packages below will use the ``Plug`` command.

All the commands and configuration below come from my `vimrc file
<https://github.com/jamescooke/dotfiles/blob/master/store/.vimrc>`_. You'll
find that I don't have a large number of plug-ins or configuration lines
compared to other more famous Vim users (cough) `Drew
<https://github.com/nelstrom/dotfiles/blob/master/bundles.vim>`_ (cough). That
is a direct result of `Kris Jenkins's Bare Bones Navigation Vim talk
<https://vimeo.com/65250028>`_ at Vim London, As a result, I have always run a
very simple Vim setup.

My relatively recent use of FZF and Ctags listed below are a direct result of
attending the most recent `Vim London meetup
<https://www.meetup.com/Vim-London/>`_ and, if you're in the London area, I
fully recommend joining and attending. Every meetup I attend, my Vim-fu
improves.


Specific Python config
----------------------

The following are my ``.vimrc`` lines for handling Python.

When searching for files with Vim, only load Python files:

.. code-block:: vim

    set suffixesadd=.py

Ignore ``pyc`` files when expanding wildcards:

.. code-block:: vim

    set wildignore=*.pyc

Don't show ``pyc`` in file lists:

.. code-block:: vim

    let g:netrw_list_hide= '.*\.pyc$'

Keep "Pythonic" tabs using 4 white spaces:

.. code-block:: vim

    set autoindent nosmartindent    " auto/smart indent
    set smarttab
    set expandtab                   " expand tabs to spaces
    set shiftwidth=4
    set softtabstop=4

I really get frustrated with tabs that look like white spaces, so I ensure
they are visible by telling Vim to show all tabs as little arrows ``▷``. This
line also ensures that end of lines are shown with a negation sign ``¬`` :

.. code-block:: vim

    set listchars=eol:¬,tab:▷\ ,

A classic "Python tell" in Vim is the 79th or 80th character highlight:

.. code-block:: vim

    set colorcolumn=80              " Show the 80th char column.
    highlight ColorColumn ctermbg=5


FZF
---

My greatest recent revelation has been the integration of `FZF
<https://github.com/junegunn/fzf>`_ to provide "quick" fuzzy searching. Most
frequently I search for files in the current git repository, open buffers and
tags.

Install FZF and get it working on your machine, then add it to your Vim
setup using `fzf.vim <https://github.com/junegunn/fzf.vim>`_:

.. code-block:: vim

    Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
    Plug 'junegunn/fzf.vim'

I've mapped my most common FZF searches to leader commands:

.. code-block:: vim

    imap <c-x><c-o> <plug>(fzf-complete-line)
    map <leader>b :Buffers<cr>
    map <leader>f :Files<cr>
    map <leader>g :GFiles<cr>
    map <leader>t :Tags<cr>

Keeping FZF's line completion on ``CTRL-x CTRL-o`` means that I can keep
access to Vim's line completion which is bound to ``CTRL-x CTRL-l`` by
default.

`Ag <https://github.com/ggreer/the_silver_searcher>`_ results integration
with FZF is next on my list, I'm still using ``Ag`` results on the command
line.


Ctags
-----

I was definitely slow to get on the `Ctags <http://ctags.sourceforge.net/>`_
bandwagon, only adding them to my workflow in the last couple of months, but
along with FZF, they have been a revelation.

TPope has published a neat trick of stashing the ``ctags`` script inside the
``.git`` folder, outlined in `his blog post here
<http://tbaggery.com/2011/08/08/effortless-ctags-with-git.html>`_. My version
of the script is inside my `git hooks configuration
<https://github.com/jamescooke/dotfiles/blob/master/store/.git_template/hooks/ctags.sh>`_
and works in combination with my `ctags config
<https://github.com/jamescooke/dotfiles/blob/master/store/.ctags>`_.

As mentioned above, I have used ``<leader>t`` to trigger an FZF-powered search
of tags:

.. code-block:: vim

    map <leader>t :Tags<cr>

The default "jump to definition under cursor" is still the default ``CTRL-]``
which, with "previous tag" ``CTRL-t`` makes it really easy to traverse code.


Visual selection
----------------

The `smartpairs plugin <https://github.com/gorkunov/smartpairs.vim>`_ is
fantastic for selecting text inside brackets, braces and parentheses and is
excellent for all languages I work with, not just Python:

.. code-block:: vim

    Plug 'gorkunov/smartpairs.vim'


Linting
-------

In general, I've used external programs to provide linting of my Python code
and so I run Vim with the current project's virtualenv active.

With `Isort <https://pypi.python.org/pypi/isort>`_ installed in the current
environment, sort the imports of the current file with ``<leader>i`` or call it
with ``:Isort`` command on a range of lines:

.. code-block:: vim

    map <leader>i :Isort<cr>
    command! -range=% Isort :<line1>,<line2>! isort -

With `flake8 <https://pypi.python.org/pypi/flake8/>`_ installed in the current
environment, lint the current file with ``F7`` as provided by `Vincent
Driessen's vim-flake8 <https://github.com/nvie/vim-flake8>`_:

.. code-block:: vim

    Plug 'nvie/vim-flake8'

Happy Vimming!

``:xa``
