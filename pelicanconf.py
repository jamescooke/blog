#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'James'
SITENAME = u'James Cooke'
TAGLINE = u'London based Python developer'
SITEURL = ''
PROFILE_IMG_URL = u'https://avatars1.githubusercontent.com/u/781059?v=3&s=200'

TIMEZONE = u'Europe/London'
DEFAULT_DATE_FORMAT = u'%b %d, %Y'

DEFAULT_LANG = u'en'
DEFAULT_CATEGORY = u'ZZZ Misc...'

# Turn off all feeds
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = [('Home', '/'), ('About', '/pages/hello-my-name-is-james.html'),]
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

TYPOGRIFY = True

THEME = '../droidstrap'
PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['related_posts']
RELATED_POSTS_MAX = 3

# Droidstrap specific config:
SHOW_SCM_LINKS = True
SCM_LINK_TEXT = 'View, comment, edit source on GitHub'
SCM_BASE_URL = 'https://github.com/jamescooke/blog/tree/master/'
