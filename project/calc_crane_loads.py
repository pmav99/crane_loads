#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calculate crane loads.

author: Panagiotis Mavrogiorgos
email : gmail, pmav99
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import logging
import logging.config
import argparse
from pprint import pprint

import crane_loads
from crane_loads import Config, OptionsBorg



class Options(OptionsBorg):
    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description=crane_loads.__short_description__,
            prog=crane_loads.__package_name__,
            epilog="",
        )

        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s ' + '%s' % crane_loads.__version__,
        )

        parser.add_argument(
            'input_file',
            action="store",
            help="The name of the file that contains the input of the crane."
        )

        parser.add_argument(
            '-c', '--config_file',
            action="store",
            dest="config_file",
            default="config.json",
            help="The location of the configuration file. Defaults to 'config.json'."
        )

        options = parser.parse_args()
        return options


def load_input(module_name):
    logger = logging.getLogger()
    logger.info("Loading input from: %r", os.path.abspath(module_name))

    # Get the module object
    input_module = __import__(os.path.splitext(module_name)[0])

    # Get the variables from the input file excluding the imports
    input_data = {}
    imports = set(["division", "print_function", "unicode_literals", "absolute_import", "tables"])
    for attribute in dir(input_module):
        if attribute.startswith("_") or attribute in imports:
            continue
        else:
            input_data[attribute] = getattr(input_module, attribute)
    logger.info("Succesfully loaded data.")
    return input_data

def main():
    # parse CLI options and read configuration file
    options = Options()
    config = Config()
    options.initialize()
    config.initialize(options.config_file)

    # initialize logging
    logging.config.dictConfig(config["logging"])
    logger = logging.getLogger()

    # get the input
    input_data = load_input(options.input_file)



if __name__ == "__main__":
    main()
