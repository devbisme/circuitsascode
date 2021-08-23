#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Dave Vandenbout'
SITENAME = 'circuits as code'
SITEURL = '/'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

THEME = 'themes/chunk'
# THEME = 'themes/pelican-simplegrey'
# THEME = 'themes/gum'
# THEME = 'foundation-default-colours'
# THEME = 'mg'

# Output path.
PATH = 'content'

# Additional paths to include in output.
STATIC_PATHS = ['images']

EXTRA_PATH_METADATA = {
        'images/favicon.ico': {'path': 'favicon.ico'}  # Copy favicon to root directory.
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Remove all footer text.
FOOTER_TEXT = " "


# Menu.
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = (
        ('Source', 'https://github.com/devbisme/circuitsascode'),
        ('Forum', 'https://github.com/xesscorp/skidl/discussions'),
        ('Blog', '/category/posts'),
        ('Library', '/api/html/index.html'),
        ('Home', '/')
)

# Blogroll
LINKS = (
        # ('About', '/pages/about.html'),
        # ('Source', 'https://github.com/devbisme/circuitsascode'),
        # ('Library', '/api/html/index.html'),
        # ('Home', '/')
        )

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
