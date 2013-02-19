# coding: utf-8

"""
    setup.py
    ~~~~~~~~

    Setup for Sickle.

    :copyright: Copright 2012 Mathias Loesch
"""

from setuptools import setup, find_packages

from sickle import __version__ as version

setup(
    name='sickle',
    version=version,
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
)