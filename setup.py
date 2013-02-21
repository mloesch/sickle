# coding: utf-8

"""
    Sickle
    ~~~~~~

    Sickle is a lightweight OAI client library for Python.

    Using Sickle
    ------------


        >>> from sickle import Sickle
        >>> client = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
        >>> response = client.ListRecords(metadataPrefix='oai_dc')

    Sickle provides different levels of abstraction for working with OAI 
    responses::

        >>> response.xml
        <Element {http://www.openarchives.org/OAI/2.0/}OAI-PMH at 0x10469a8c0>
        >>> response.raw
        u'<?xml version=\'1.0\' encoding ...'

    And a convenient way for iterating through all records of a repository:

        >>> records = response.iter()
        >>> records.next()
        <Element {http://www.openarchives.org/OAI/2.0/}record at 0x1051b3b90>

"""

from setuptools import setup, find_packages


setup(
    name='Sickle',
    version='0.1',
    url='http://github.com/mloesch/sickle',
    license='BSD',
    author='Mathias Loesch',
    author_email='mathias.loesch@uni-bielefeld.de',
    description='A lightweight OAI client library for Python',
    long_description=__doc__,
    packages=['sickle'],
    platforms='any',
    install_requires=[
        'requests>=1.1.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Markup :: XML',
    ],
    zip_safe=False,
)
