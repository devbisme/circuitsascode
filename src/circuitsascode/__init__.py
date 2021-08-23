# The MIT License (MIT) - Copyright (c) 2021 xesscorp

"""
Categorized collections of circuits.
"""

import sys

import pint

# Create a shortcut name for "circuitsascode".
sys.modules["casc"] = sys.modules["circuitsascode"]

# For electrical units like ohms, volts, etc.
units = pint.UnitRegistry()

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
