:mod:`OpenEXR` --- Read and write EXR format images
===================================================

.. module:: OpenEXR
   :synopsis: Read and write EXR format images

Available Types
---------------

.. class:: InputFile

   The :class:`InputFile` object is used to read an EXR file.

   .. doctest::
      :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

      >>> import OpenEXR
      >>> print len(OpenEXR.InputFile("GoldenGate.exr").channel('R')), "bytes of red data"
      2170640 bytes of red data

   The following data items and methods are supported:

   .. method:: InputFile.header() -> dict

      Return the header of the open file. The header is a dictionary as described below.

   .. index:: scan-line, format, string, pixel_type

   .. method:: channel(cname[, pixel_type[, scanLine1[, scanLine2]]]) -> string

       Read a channel from the OpenEXR image. *cname* is the name
       of the channel in the image, for example "R".
       This method returns
       channel data in the format specified by *pixel_type* (see
       :class:`Imath.PixelType`), or the channel's format specified
       in the image itself by default.
       If *scanLine1* and *scanLine2* are not supplied, then the
       method reads the entire image. Note that this method returns
       the channel data as a Python string: the caller must then convert
       it to the appropriate format as necessary.

   .. index:: destructor, convenience, exit

   .. method:: close()

       Close the open file. Calling this method is mandatory, otherwise
       the file will be incomplete.  However, as a convenience, the
       object's destructor calls this method, so any open files are
       automatically closed at program exit.

   .. index:: complete

   .. method:: isComplete()

       isComplete() returns True if all pixels in the data window are
       present in the input file, or False if any pixels are missing.
       (Another program may still be busy writing the file, or file
       writing may have been aborted prematurely.)

.. class:: OutputFile(filename, header)

   Creates the EXR file *filename*, with given *header*.  *header*
   contains the image's properties represented as a dictionary - for example the one created by 
   the convenience function :func:`Header`.

   .. doctest::

      >>> import OpenEXR, array
      >>> data = array.array('f', [ 1.0 ] * (640 * 480)).tostring()
      >>> exr = OpenEXR.OutputFile("out.exr", OpenEXR.Header(640,480))
      >>> exr.writePixels({'R': data, 'G': data, 'B': data})

   The following data items and methods are supported:

   .. index:: scan-line

   .. method:: writePixels(dict, [scanlines])

       Write the specified channels to the OpenEXR image. *dict*
       specifies multiple channels. If *scanlines* is not specified,
       then the entire image is assumed. dict specifies each channel's
       data as channel:data, where channel and data are both strings.
       This method uses the file's header
       to determine the format of the data (FLOAT, HALF or UINT) for
       each channel. If the string data is not of the appropriate size,
       this method raises an exception.

   .. index:: scan-line

   .. method:: currentScanLine() -> int

       Return the current scan line being written.

   .. index:: destructor, convenience

   .. method:: close()

       Close the open file.  This method may be called multiple times.
       As a convenience, the object's destructor calls this method.

Available Functions
-------------------

.. index:: valid

.. function:: isOpenExrFile(filename) -> bool

   Returns True if the *filename* exists, is readable, and contains a valid EXR image.

   .. doctest::

      >>> import OpenEXR
      >>> print OpenEXR.isOpenExrFile("no-such-file")
      False
      >>> print OpenEXR.isOpenExrFile("lena.jpg")
      False
      >>> print OpenEXR.isOpenExrFile("GoldenGate.exr")
      True
   
   Note that a file may may valid, but not complete.  To check if a file is complete, use :meth:`InputFile.isComplete`.

.. index:: convenience

.. function:: Header(width, height) -> dict

   Convenience function that creates the EXR header for an image
   of size *width* x *height* with EXR mandatory entries set to
   appropriate defaults.  An EXR header is a dictionary -
   see :ref:`headers` for details of legal header contents.

   .. doctest::
      :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

      >>> import OpenEXR
      >>> print OpenEXR.Header(640,480)
      {'compression': ZIP_COMPRESSION,
       'pixelAspectRatio': 1.0,
       'displayWindow': (0, 0) - (639, 479),
       'channels': {'R': FLOAT (1, 1), 'B': FLOAT (1, 1), 'G': FLOAT (1, 1)},
       'dataWindow': (0, 0) - (639, 479),
       'screenWindowCenter': (0.0, 0.0),
       'screenWindowWidth': 1.0,
       'lineOrder': INCREASING_Y}


.. _headers:

EXR header values
-----------------

.. index::
   pair: header; values
   single: attribute
   single: types
   single: dictionary

This module represents EXR headers as regular Python dictionaries.
In this dictionary the keys are strings, and the values are such
that OpenEXR can determine their type. The module :mod:`Imath` provides
many of the classes for attribute types.

   .. doctest::
      :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

      >>> import OpenEXR
      >>> print OpenEXR.InputFile("GoldenGate.exr").header()
      {'tiles': None,
       'capDate': '2004:01:04 18:10:00',
       'compression': PIZ_COMPRESSION,
       'latitude': 37.827701568603516,
       'pixelAspectRatio': 1.0,
       'altitude': 274.5,
       'displayWindow': (0, 0) - (1261, 859),
       'focus': inf,
       'comments': 'View from Hawk Hill towards San Francisco',
       'screenWindowWidth': 1.1499999761581421,
       'channels': {'R': HALF (1, 1), 'B': HALF (1, 1), 'G': HALF (1, 1)},
       'isoSpeed': 50.0,
       'utcOffset': 28800.0,
       'longitude': -122.49960327148438,
       'dataWindow': (0, 0) - (1261, 859),
       'screenWindowCenter': (0.0, 0.0),
       'aperture': 2.7999999523162842,
       'preview': <Imath.PreviewImage instance 100x68>,
       'owner': 'Copyright 2004 Industrial Light & Magic',
       'expTime': 8.0,
       'lineOrder': INCREASING_Y}

   Values in the dictionary may be:

   .. index::
      single: header; string

   string

      ::

         header['owner'] = 'Copyright 2007 James Bowman'

   .. index::
      single: header; float

   float

      ::

         header['isoSpeed'] = 50.0

   .. index::
      single: header; int

   int

      ::

         header['version'] = 1001

   .. index::
      single: header; dict

   dict

      A dict represents the image's channels. In the dict, the keys are the channel names, and the values are of class :class:`Imath.Channel`::

         header['channels'] = { 'L' : Imath.Channel(PixelType(OpenEXR.HALF)),
                                'Z' : Imath.Channel(PixelType(OpenEXR.FLOAT))}

   :class:`Imath.Box2i`

      ::

         header['dataWindow'] = Imath.Box2i(Imath.point(0,0), Imath.point(640,480))

   :class:`Imath.Box2f`

      ::

         header['regionOfInterest'] = Imath.Box2f(Imath.point(75.0,75.0),
                                                  Imath.point(100.0,100.0))


   :class:`Imath.V2f`

      ::

         header['originMarker'] = Imath.point(0.378, 0.878)

   :class:`Imath.LineOrder`

      ::

         header['lineOrder'] = Imath.LineOrder(Imath.LineOrder.INCREASING_Y)

   :class:`Imath.PreviewImage`

      A preview image, specified by height, width, and a string of length 4*width*height. The pixels are in RGBA order.::

         header['preview'] = Imath.PreviewImage(320,200,pixels)

      or to use a `PIL <http://www.pythonware.com/products/pil/>`_  image as an EXR preview::

         header['preview'] = Imath.PreviewImage(im.size[0], im.size[1], im.convert("RGBA").tostring())

   :class:`Imath.Compression`

      ::

         header['Compression'] = Imath.Compression(Imath.Compression.PIZ_COMPRESSION)
