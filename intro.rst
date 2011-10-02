Introduction and Cookbook
=========================

.. index:: ILM, Industrial Light & Magic, high dynamic range, floating point

`OpenEXR <http://www.openexr.com/>`_ is an image format developed by
`ILM <http://www.ilm.com/>`_.
Its main innovation is
support for high dynamic range; it supports floating point pixels.

This module provides Python bindings for the OpenEXR
`C++ libraries <http://www.openexr.com/ReadingAndWritingImageFiles.pdf>`_.
They allow you to read and write OpenEXR files from Python.

Note that this module only loads and stores image data. It does not
do any image manipulation operations. For that you might want to
use one of these imaging or math packages.

Interfacing with other packages
-------------------------------

.. index:: PIL, NumPy, vop, OpenCV, HALF, UINT, FLOAT

* Python's standard `array <http://docs.python.org/library/array.html>`_ module.  You can access the raw data of FLOAT and UINT images as a 1D array.

   .. doctest::
      :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

      >>> import OpenEXR, Imath, array
      >>> pt = Imath.PixelType(Imath.PixelType.FLOAT)
      >>> redstr = OpenEXR.InputFile("GoldenGate.exr").channel('R', pt)
      >>> red = array.array('f', redstr)
      >>> print red[0]
      0.0612182617188

* The `Python Imaging Library <http://www.pythonware.com/library/pil/handbook/index.htm>`_. This library supports a single FLOAT channel image format, as a 2D array.

   .. doctest::
      :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

      >>> import OpenEXR, Imath, Image
      >>> pt = Imath.PixelType(Imath.PixelType.FLOAT)
      >>> golden = OpenEXR.InputFile("GoldenGate.exr")
      >>> dw = golden.header()['dataWindow']
      >>> size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
      >>> redstr = golden.channel('R', pt)
      >>> red = Image.fromstring("F", size, redstr)
      >>> print red.getpixel((0, 0))
      0.0612182617188

* `Numeric or NumPy <http://numpy.scipy.org/>`_. It's just math, so you will have to write your own imaging operations. Supports UINT and FLOAT formats.  Supports 2D arrays.

   .. doctest::
      :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

      >>> import OpenEXR, Imath, numpy
      >>> pt = Imath.PixelType(Imath.PixelType.FLOAT)
      >>> golden = OpenEXR.InputFile("GoldenGate.exr")
      >>> dw = golden.header()['dataWindow']
      >>> size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
      >>> redstr = golden.channel('R', pt)
      >>> red = numpy.fromstring(redstr, dtype = numpy.float32)
      >>> red.shape = (size[1], size[0]) # Numpy arrays are (row, col)
      >>> print red[0, 0]
      0.0612182617188

  As of version 1.6.0 NumPy supports HALF float via its float16 type::

      import numpy
      import OpenEXR
      import Imath

      pixels = numpy.random.rand(640, 480).astype(numpy.float16).tostring()
      HEADER = OpenEXR.Header(640,480)
      half_chan = Imath.Channel(Imath.PixelType(Imath.PixelType.HALF))
      HEADER['channels'] = dict([(c, half_chan) for c in "RGB"])
      exr = OpenEXR.OutputFile("out.exr", HEADER)
      exr.writePixels({'R': pixels, 'G': pixels, 'B': pixels})
      exr.close()
      print OpenEXR.InputFile("out.exr").header()

* Module `vop <http://www.excamera.com/articles/25/vop.html>`_. NumPy subset, but faster. Supports FLOAT and HALF.  1D arrays only.

   .. doctest::
      :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

      >>> import OpenEXR, Imath, vop
      >>> pt = Imath.PixelType(Imath.PixelType.FLOAT)
      >>> redstr = OpenEXR.InputFile("GoldenGate.exr").channel('R', pt)
      >>> red = vop.fromstring(redstr)
      >>> print red[0]
      0.0612182617188

* `OpenCV <http://opencv.willowgarage.com/wiki/>`_.  Supports multi channel UINT and FLOAT formats.  Supports 2D arrays.

   .. doctest::
      :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

      >>> import OpenEXR, Imath, cv
      >>> pt = Imath.PixelType(Imath.PixelType.FLOAT)
      >>> golden = OpenEXR.InputFile("GoldenGate.exr")
      >>> dw = golden.header()['dataWindow']
      >>> size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
      >>> redstr = golden.channel('R', pt)
      >>> red = cv.CreateMat(size[1], size[0], cv.CV_32FC1)
      >>> cv.SetData(red, redstr)
      >>> print red[0, 0]
      0.0612182617188

Conversions
===========

EXR to EXR
----------

To modify a header field, you can read the file, modify the header, then write a new file with the same data and the modified header:

.. literalinclude:: demo2.py
    :language: python

OpenEXR to jpg
--------------

This is a simple command-line tool to turn an EXR file into a jpg file.  It finds the darkest and lightest pixels in the floating-point EXR image, then normalizes all image pixels to the range 0-255.

.. literalinclude:: exr2jpg.py
    :language: python
