#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'James'
SITENAME = 'James Cooke'
TAGLINE = 'Brighton based Python developer'
SITEURL = ''
PROFILE_IMG_URL = '/images/coding_cooke_ltd.png'

TIMEZONE = 'Europe/London'
DEFAULT_DATE_FORMAT = '%b %d, %Y'

DEFAULT_LANG = 'en'
DEFAULT_CATEGORY = 'ZZZ Misc...'

STATIC_PATHS = ['images', 'docs']

# Turn off all feeds
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = [
    ('Home', '/'),
    ('About', '/pages/hello-my-name-is-james.html'),
    ('Coding Cooke', '/pages/coding-cooke.html'),
]
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

TYPOGRIFY = True

THEME = '../droidstrap'
PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['related_posts', 'render_math']
RELATED_POSTS_MAX = 3

# Droidstrap specific config:
SHOW_SCM_LINKS = True
SCM_LINK_TEXT = 'View, comment, edit source on GitHub'
SCM_BASE_URL = 'https://github.com/jamescooke/blog/tree/master/'
