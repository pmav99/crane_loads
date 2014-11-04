#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Panagiotis Mavrogiorgos
# email : gmail, pmav99

"""
A Package that calculates crane loads.

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

# Version
__major__ = 0  # for major interface/format changes
__minor__ = 1  # for minor interface/format changes
__release__ = 0  # for tweaks, bug-fixes, or development

# package information
__package_name__ = "crane_loads"
__description__ = __doc__
__short_description__ = "A package that calculates crane loads."
__version__ = "%d.%d.%d" % (__major__, __minor__, __release__)
__license__ = "BSD"
__url__ = "http://bitbucket.org/pmav99/%s" % __package_name__
__download_url__ = "http://bitbucket.org/pmav99/%s/downloads" % __package_name__
__author__ = "Panagiotis Mavrogiorgos"
__author_email__ = "gmail pmav99"
__platforms__ = ("Linux",)

# Package imports
from .utils import OptionsBorg, Config
from .loads import CraneLoads
from .output import LaTeXOutput
