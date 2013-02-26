# coding: utf-8

"""
    Sickle
    ~~~~~~

    Sickle is a lightweight OAI client library for Python.

    Using Sickle
    ------------

        >>> from sickle import Sickle
        >>> client = Sickle('http://elis.da.ulcc.ac.uk/cgi/oai2')
        >>> records = client.ListRecords(metadataPrefix='oai_dc')

    Sickle provides a convenient way for iterating through all records of a repository:

        >>> records.next()
        <Record ...>

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
        'lxml',
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
