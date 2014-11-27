# coding: utf-8

from setuptools import setup, find_packages


setup(
    name='Sickle',
    version='0.4',
    url='http://github.com/mloesch/sickle',
    license='BSD',
    author='Mathias Loesch',
    author_email='mathias.loesch@uni-bielefeld.de',
    description='A lightweight OAI client library for Python',
    long_description=open('README.rst').read() + '\n\n' +
    open('CHANGES.rst').read(),
    packages=['sickle'],
    platforms='any',
    setup_requires=[
        'nose>=1.0',
        'mock>=1.0.1'],
    install_requires=[
        'requests>=1.1.0',
        'lxml>=3.2.3'],
    classifiers=[
        'Development Status :: 4 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Markup :: XML',
    ],
    test_suite = "sickle.tests",
    keywords="oai oai-pmh",
    zip_safe=False,
)
