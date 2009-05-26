Introduction
============

.. index:: ILM, Industrial Light & Magic, high dynamic range, floating point

`OpenEXR <http://www.openexr.com/>`_ is an image format developed by
`ILM <http://www.ilm.com/>`_.
Its main innovation is
support for high dynamic range; it supports floating point pixels.

This module provides Python bindings for the OpenEXR
`C++ libraries <http://www.openexr.com/ReadingAndWritingImageFiles-1.2.x.pdf>`_.
They allow you to read and write OpenEXR files from Python.

Note that this module only loads and stores images. It does not do
any image manipulation operations. For that you might want to use
one of:

.. index:: PIL, NumPy, vop, OpenCV, HALF, UINT, FLOAT

* Python's standard `array <http://docs.python.org/library/array.html>`_ module.  You can access the raw data of FLOAT and UINT images.
* The `Python Imaging Library <http://www.pythonware.com/library/pil/handbook/index.htm>`_. This library supports a single FLOAT channel image format.
* `Numeric or NumPy <http://numpy.scipy.org/>`_. It's just math, so you will have to write your own imaging operations. Supports UINT and FLOAT formats.
* Module `vop <http://www.excamera.com/articles/25/vop.html>`_. NumPy subset, but faster. Supports FLOAT and HALF. 
* `OpenCV <http://opencv.willowgarage.com/wiki/>`_.  Supports multi channel UINT and FLOAT formats.

