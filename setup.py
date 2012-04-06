# mockextras.fluent
# Matchers and Stubs for mock.
# Copyright (C) 2012 Andrew Burrows
# E-mail: burrowsa AT gmail DOT com

# mockextras 0.0.0
# https://github.com/burrowsa/mockextras

# Released subject to the BSD License
# Please see https://github.com/burrowsa/mockextras/blob/master/LICENSE.txt

if __name__ == "__main__":
    params = dict(name="mockextras",
        version="0.0.0",
        description="Extensions to the mock library",
        author="Andrew Burrows",
        author_email="burrowsa@gmail.com",
        url="https://github.com/burrowsa/mockextras",
        packages=['mockextras'],
        license="BSD",
        long_description="""The mockextras library is designed to be used with the mock library by Michael Foord 
(http://www.voidspace.org.uk/python/mock/). mockextras adds a number of features that
are found in other mocking libraries namely:

* matchers
* stubs
* a fluent API for the configuration of stubs""",
        classifiers=["Development Status :: 2 - Pre-Alpha",
                     "Environment :: Console",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: BSD License",
                     "Programming Language :: Python",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: Implementation :: CPython",
                     "Operating System :: OS Independent",
                     "Topic :: Software Development :: Libraries",
                     "Topic :: Software Development :: Libraries :: Python Modules",
                     "Topic :: Software Development :: Testing"])

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup
    else:
        params['install_requires '] = ['mock>=0.8.0']

    setup(**params)
