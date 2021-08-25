#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

from pelicanconf import *

sys.path.append(os.curdir)

# If your site is available via HTTPS, make sure SITEURL begins with https://
# SITEURL = 'https://devbisme.github.io/circuitsascode'
# SITEURL = "https://devbisme.github.io/circuitsascode/docs/pelicansite/output"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

# MENUITEMS = (
#     ("Source", "https://github.com/devbisme/circuitsascode"),
#     ("Forum", "https://github.com/xesscorp/skidl/discussions"),
#     ("Blog", f"{SITEURL}/category/posts"),
#     ("Library", f"{SITEURL}/api/html/index.html"),
#     ("Home", f"{SITEURL}/"),
# )

# Following items are often useful when publishing

# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""