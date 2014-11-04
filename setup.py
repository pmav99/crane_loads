#!/usr/bin/env python3

import crane_loads
from distutils.core import setup


setup(
    name = crane_loads.__name__,
    packages = [crane_loads.__name__],
    scripts = ['bin/cranes_to_tex'],
    version = crane_loads.__version__,
    description = crane_loads.__description__,
    long_description = """.""",
    author = crane_loads.__author__,
    author_email = crane_loads.__author_email__,
    license = crane_loads.__license__,
    platforms = crane_loads.__platforms__,
    url = crane_loads.__url__,
    download_url = crane_loads.__download_url__,
    keywords = [
        'civil' 'engineer', 'loads', 'eurocodes', 'eurocode', 'cranes'
    ],
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python 3',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Natural Language :: English',
        'Natural Language :: Greek',
        'Topic :: Utilities'
    ],
)

