#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Panagiotis Mavrogiorgos
#email : gmail, pmav99

"""
A module for handling crane loads output

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import sys
import shutil
import logging
import tempfile
import subprocess
from io import StringIO

from jinja2 import Environment, PackageLoader



class CraneOutput(object):
    pass


class LaTeXOutput(CraneOutput):
    skewing_templates = {
        "IFF": "IFF.tex",
        "IFM": "IFM.tex",
        "CFF": "CFF.tex",
        "CFM": "CFM.tex",
    }

    known_languages = {
        "en": "en",
        "gr": "gr",
    }

    def __init__(self, data, language, engine="xelatex", output_filename=None):
        self.logger = logging.getLogger().getChild("latex")

        if language not in self.known_languages:
            msg = "Unknown language <%s>. Please choose one of: %r" % language, self.known_languages.keys()
            self.logger.error(msg)
            raise ValueError(msg)

        self.data = data
        self.engine=engine
        self.output_filename = output_filename

        # get templates
        template_path = os.path.join('templates', language)
        self.env = Environment(loader=PackageLoader('crane_loads', template_path))

    def create_tex(self):
        # we have to determine which skewing template to use during runtime.
        skewing_template_name = self.skewing_templates[self.data["RT"]]

        # get templates
        self.logger.info("Loading templates.")
        preamble_template = self.env.get_template("preamble.tex")
        input_template = self.env.get_template("input.tex")
        forces_template = self.env.get_template("forces.tex")
        skewing_template = self.env.get_template(skewing_template_name)
        fatigue_template = self.env.get_template("fatigue.tex")
        table_template = self.env.get_template("table.tex")
        self.logger.info("Loaded templates.")

        # render tex document
        self.logger.info("Rendering templates.")
        input_text = input_template.render(**self.data)
        forces_text = forces_template.render(**self.data)
        skewing_text = skewing_template.render(**self.data)
        fatigue_text = fatigue_template.render(**self.data)
        table_text = table_template.render(**self.data)
        self.logger.info("Rendered templates.")

        self.logger.info("Creating tex document.")
        tex_document = preamble_template.render(
            input=input_text,
            forces=forces_text,
            skewing=skewing_text,
            fatigue=fatigue_text,
            table=table_text,
        )
        self.logger.info("Document created successfully!")
        return tex_document

    def _compile_document(self):
        try:
            subprocess.call([self.engine, self._tex_filename])
            subprocess.call([self.engine, self._tex_filename])
        except Exception as exc:
            self.logger.exception("%s: Something went wrong while compiling: %s", self.engine, self._tex_filename)
            raise exc

    def _create_build_dir(self):
        # create build dir
        try:
            build_dir = tempfile.mkdtemp()
        except Exception as exc:
            self.logger.exception("Couldn't create a temp dir.")
            raise exc

        else:
            self.logger.info("Created a build directory at: %s", build_dir)
            return build_dir

    def _clean_up(self, directory):
        try:
            shutil.rmtree(directory)
        except Exception as exc:
            self.logger.exception("Couldn't clean up: %s", directory)
            raise exc

    def compile(self):
        """
        Create the build dir, render the tex file, compile it and get the filenames
        """
        build_dir = self._create_build_dir()
        os.chdir(build_dir)
        self._tex_filename = os.path.join(build_dir, "foo.tex")
        self._pdf_filename = os.path.splitext(self._tex_filename)[0] + ".pdf"
        self.logger.debug("tex: %s", self._tex_filename)
        self.logger.debug("pdf: %s", self._pdf_filename)
        self._write_file_to_disk()
        self._compile_document()
        return self._pdf_filename

    def _write_file_to_disk(self):
        tex_document = self.create_tex()
        try:
            with open(self._tex_filename, "w") as fd:
                fd.write(tex_document)
        except Exception as exc:
            self.logger.exception("Something went wrong while writing tex file to disk:",
                                  self._tex_filename)
            raise exc
