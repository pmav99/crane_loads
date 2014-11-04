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

# Standard Library
import os
import logging
import logging.config
import argparse
import subprocess
from pprint import pprint

# Our libraries
import crane_loads
from crane_loads import Config, OptionsBorg, CraneLoads, LaTeXOutput


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


def main():
    # parse CLI options and read configuration file
    options = Options()
    config = Config()
    options.initialize()
    config.initialize(options.config_file)

    # initialize logging
    logging.config.dictConfig(config["logging"])
    logger = logging.getLogger()

    # Calculate crane loads.
    crane_loads = CraneLoads.from_module(options.input_file)
    crane_loads.calc()

    # Create tex output
    latex = LaTeXOutput(crane_loads.data, language="en")
    pdf_file = latex.compile()
    print(pdf_file)

    #subprocess.call(["evince", pdf_file])


if __name__ == "__main__":
    main()
