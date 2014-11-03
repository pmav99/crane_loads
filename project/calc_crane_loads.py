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
from pprint import pprint

# 3rd party libraries
from jinja2 import Environment, PackageLoader

# Our libraries
import crane_loads
from crane_loads import Config, OptionsBorg, CraneLoads


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

    # initialize instance
    loads = CraneLoads.from_module(options.input_file)
    loads.calc()
    tex = loads._create_tex()

    #with open("/tmp/foo.tex", "w") as fd:
        #fd.write(tex)

    #import os
    #os.system("xelatex /tmp/foo.tex; mv ./foo.pdf /tmp/; rmtex")



if __name__ == "__main__":
    main()
