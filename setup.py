# mockextras.fluent
# Matchers and Stubs for mock.
# Copyright (C) 2012 Andrew Burrows
# E-mail: burrowsa AT gmail DOT com

# mockextras 0.0.0
# https://github.com/burrowsa/mockextras

# Released subject to the BSD License
# Please see https://github.com/burrowsa/mockextras/blob/master/LICENSE.txt

from distutils.core import setup

setup(name = "mockextras",
    version = "0.0.0",
    description = "Extensions to the mock library",
    author = "Andrew Burrows",
    author_email = "burrowsa@gmail.com",
    url = "https://github.com/burrowsa/mockextras",
    packages = ['mockextras'],
    license = "BSD",
    long_description = """The mockextras library is designed to be used with the mock library by Michael Ford 
(http://www.voidspace.org.uk/python/mock/). mockextras adds a number of features that
are found in other mocking libraries namely:

* matchers
* stubs
* a fluent API for the configuration of stubs""",
    classifiers = ["Classifier: Development Status :: 2 - Pre-Alpha",
"Classifier: Environment :: Console",
"Classifier: Intended Audience :: Developers",
"Classifier: License :: OSI Approved :: BSD License",
"Classifier: Programming Language :: Python",
"Classifier: Programming Language :: Python :: 2.7",
"Classifier: Programming Language :: Python :: Implementation :: CPython",
"Classifier: Operating System :: OS Independent",
"Classifier: Topic :: Software Development :: Libraries",
"Classifier: Topic :: Software Development :: Libraries :: Python Modules",
"Classifier: Topic :: Software Development :: Testing"]) 