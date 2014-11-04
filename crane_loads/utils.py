#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

author: Panagiotis Mavrogiorgos
email : gmail, pmav99
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import abc
import json
import codecs
import collections

from pprint import pformat

# setup logging
import logging
logger = logging.getLogger(__name__)


class Borg(object):
    """
    Borg instances share the same state among all their instances.

    If we need to subclass a Borg, and we want the subclasses' instances
    to have a different state then the subclass must redefine `_shared_state`!
    """
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        instance = super(Borg, cls).__new__(cls, *args, **kwargs)
        instance.__dict__ = cls._shared_state
        return instance


class MutableMapping(collections.MutableMapping):
    """
    A dictionary subclass that for all apparent uses behaves like a dictionary!

    http://stackoverflow.com/a/3387975/592289

    """

    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        """ Pretty printing is nice! """
        return pformat({k: v for k, v in self.__dict__.items() if not k.startswith("_")})


class Config(Borg, MutableMapping):
    """
    A Borg that uses a dictionary's interface and that gets populated
    by parsing the JSON configuration file that is passed as an
    argument to its initialize() method.
    """

    _shared_state = {}

    def initialize(self, config_file):
        # the loggers configured here will be disabled later on when we properly
        # configure logging. We only use this one in order to log the location of
        # the configuration file.
        logging.basicConfig(level="INFO")
        logging.info("configuration file: %s", os.path.abspath(config_file))
        with codecs.open(config_file, "rb", "utf-8") as fd:
            self.__dict__.update(json.load(fd))


class OptionsBorg(Borg, MutableMapping):
    """
    CLI options Borg.

    It has to be sublcassed and subclasses must implement a parse_arugments() method.
    """

    _shared_state = {}

    def initialize(self):
        d = self.__dict__
        cli_args = self.parse_arguments()

        if isinstance(cli_args, dict):
            d.update(cli_args)
        else:
            d.update({key: value for key, value in cli_args.__dict__.items()})

    @abc.abstractmethod
    def parse_arguments(self, *args, **kwargs):
        pass
