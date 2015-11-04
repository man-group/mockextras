# mockextras.fluent
# Matchers and Stubs for mock.
# Copyright (C) 2012-2015 Man AHL
# E-mail: ManAHLTech AT ahl DOT com

# mockextras 1.0.0
# https://github.com/manahl/mockextras

# Released subject to the BSD License
# Please see https://github.com/manahl/mockextras/blob/master/LICENSE.txt

if __name__ == "__main__":
    params = dict(name="mockextras",
        version="1.0.1",
        description="Extensions to the mock library",
        author="Man AHL",
        author_email="ManAHLTech@ahl.com",
        url="https://github.com/manahl/mockextras",
        packages=['mockextras'],
        license="BSD",
        long_description="""The mockextras library is designed to be used with the unittest.mock library in python 3 or the mock
backport of this (http://www.voidspace.org.uk/python/mock/) in python 2. The mockextras library adds
a number of features that are found in other mocking libraries namely:

* a fluent API for the configuration of stubs
* stubs
* matchers

The documentation is here: http://mockextras.readthedocs.org/
and the source is here: http://github.com/manahl/mockextras""",
        classifiers=["Development Status :: 5 - Production/Stable",
                     "Environment :: Console",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: BSD License",
                     "Programming Language :: Python",
                     "Programming Language :: Python :: 2.6",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3.3",
                     "Programming Language :: Python :: 3.4",
                     "Programming Language :: Python :: 3.5",
                     "Programming Language :: Python :: Implementation :: CPython",
                     "Programming Language :: Python :: Implementation :: PyPy",
                     "Operating System :: OS Independent",
                     "Topic :: Software Development :: Libraries",
                     "Topic :: Software Development :: Libraries :: Python Modules"])

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup
    else:
        params['install_requires'] = []

    try:
        from unittest import mock
    except ImportError:
        params['install_requires'] += ['mock>=0.8.0']

    setup(**params)
