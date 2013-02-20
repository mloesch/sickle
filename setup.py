# coding: utf-8

"""
    setup.py
    ~~~~~~~~

    Setup for Sickle.

    :copyright: Copright 2012 Mathias Loesch
"""

from setuptools import setup, find_packages


setup(
    name='sickle',
    version='0.1',
    long_description=__doc__,
    install_requires=[
        'requests>=1.1.0',
    ],
    packages=find_packages(),
    zip_safe=False,
)
