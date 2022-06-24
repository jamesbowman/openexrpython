OpenEXR bindings for Python
===========================

[![Build Status](https://travis-ci.org/jamesbowman/openexrpython.svg?branch=master)](https://travis-ci.org/jamesbowman/openexrpython)

This code is no longer maintained -- see https://github.com/sanguinariojoe/pip-openexr

See homepage at http://www.excamera.com/sphinx/articles-openexr.html

## Requirements

To build from source, a C++ compiler and libraries and development headers for OpenEXR and zlib are required. In Ubuntu, the `g++`, `libopenexr-dev` and `zlib1g-dev` packages suffice all requirements. In OSX, the Homebrew packages `openexr` and `zlib` will suffice.

For the latest release, run:

    pip install openexr

In case the PyPi package is not updated and you want to install from the master branch, you can do the following:

    pip install git+https://github.com/jamesbowman/openexrpython.git

If you prefer, you can clone it and run the `setup.py` file as well. Use the following
commands to get a copy from Github and do the installation:

    git clone https://github.com/jamesbowman/openexrpython
    pip install ./openexrpython
