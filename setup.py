# coding: utf-8

from setuptools import setup, find_packages


setup(
    name='Sickle',
    version='0.3',
    url='http://github.com/mloesch/sickle',
    license='BSD',
    author='Mathias Loesch',
    author_email='mathias.loesch@uni-bielefeld.de',
    description='A lightweight OAI client library for Python',
    long_description=open('README.rst').read() + '\n\n' +
    open('CHANGES.rst').read(),
    packages=['sickle'],
    platforms='any',
    setup_requires=['nose>=1.0'],
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
    keywords="oai oai-pmh",
    zip_safe=False,
)
