#!/usr/bin/env python

from distutils.core import setup

import mygeocoder

def get_long_description():
    """
    Return the contents of the README file.
    """
    try:
        return open('README.rst').read()
    except:
        pass  # Required to install using pip (won't have README then)

setup(
    name = 'mygeocoder',
    version = mygeocoder.__version__,
    description = "Python wrapper around the Tiger Geocoder that comes with PostGIS 2+.",
    long_description = get_long_description(),
    author = "Eric Palakovich Carr",
    author_email = "carreric@gmail.com",
    license = "MIT",
    url = "https://github.com/bigsassy/geocoder",
    packages = [
        'mygeocoder',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ]
)
