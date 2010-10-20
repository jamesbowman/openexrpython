"""
:mod:`Imath` --- Support types for OpenEXR library
==================================================
"""

class chromaticity(object):
    """Store chromaticity coordinates in *x* and *y*."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return repr((self.x, self.y))
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

class point(object):
    """Point is a 2D point, with members *x* and *y*."""
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
    def __repr__(self):
        return repr((self.x, self.y))
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

class V2i(point):
    """V2i is a 2D point, with members *x* and *y*."""
    pass

class V2f(point):
    """V2f is a 2D point, with members *x* and *y*."""
    pass

class Box:
    """Box is a 2D box, specified by its two corners *min* and *max*, both of which are :class:`point` """
    def __init__(self, min = None, max = None):
        self.min = min
        self.max = max
    def __repr__(self):
        return repr(self.min) + " - " + repr(self.max)
    def __eq__(self, other):
        return (self.min, self.max) == (other.min, other.max)

class Box2i(Box):
    """Box2i is a 2D box, specified by its two corners *min* and *max*."""
    pass

class Box2f(Box):
    """Box2f is a 2D box, specified by its two corners *min* and *max*."""
    pass

class Chromaticities:
    """
    Chromaticities holds the set of chromaticity coordinates for *red*, *green*, *blue*, and *white*.
    Each primary is a :class:`chromaticity`.
    """
    def __init__(self, red = None, green = None, blue = None, white = None):
        self.red   = red
        self.green = green
        self.blue  = blue
        self.white = white
    def __repr__(self):
        return repr(self.red) + " " + repr(self.green) + " " + repr(self.blue) + " " + repr(self.white)

class Enumerated(object):
    def __init__(self, v):
        if v in self.names:
            self.v = eval("self." + v)
        else:
            self.v = v
    def __repr__(self):
        return self.names[self.v]
    def __cmp__(self, other):
        return self.v - other.v

class LineOrder(Enumerated):
    """
    .. index:: INCREASING_Y, DECREASING_Y, RANDOM_Y

    LineOrder can have three possible values:
    ``INCREASING_Y``,
    ``DECREASING_Y``,
    ``RANDOM_Y``.

    .. doctest::
    
       >>> import Imath
       >>> print Imath.LineOrder(Imath.LineOrder.DECREASING_Y)
       DECREASING_Y
    """
    INCREASING_Y = 0
    DECREASING_Y = 1
    RANDOM_Y	 = 2
    names = ["INCREASING_Y", "DECREASING_Y", "RANDOM_Y"]

class Compression(Enumerated):
    """
    .. index:: NO_COMPRESSION, RLE_COMPRESSION, ZIPS_COMPRESSION, ZIP_COMPRESSION, PIZ_COMPRESSION, PXR24_COMPRESSION

    Compression can have possible values:
    ``NO_COMPRESSION``,
    ``RLE_COMPRESSION``,
    ``ZIPS_COMPRESSION``,
    ``ZIP_COMPRESSION``,
    ``PIZ_COMPRESSION``,
    ``PXR24_COMPRESSION``.

    .. doctest::
    
       >>> import Imath
       >>> print Imath.Compression(Imath.Compression.RLE_COMPRESSION)
       RLE_COMPRESSION
    """
    NO_COMPRESSION  = 0
    RLE_COMPRESSION = 1
    ZIPS_COMPRESSION = 2
    ZIP_COMPRESSION = 3
    PIZ_COMPRESSION = 4
    PXR24_COMPRESSION = 5
    names = [ "NO_COMPRESSION", "RLE_COMPRESSION", "ZIPS_COMPRESSION", "ZIP_COMPRESSION", "PIZ_COMPRESSION", "PXR24_COMPRESSION"]

class PixelType(Enumerated):
    """
    .. index:: UINT, HALF, FLOAT

    PixelType can have possible values ``UINT``, ``HALF``, ``FLOAT``.

    .. doctest::
    
       >>> import Imath
       >>> print Imath.PixelType(Imath.PixelType.HALF)
       HALF
    """
    UINT  = 0
    HALF  = 1
    FLOAT = 2
    names = ["UINT", "HALF", "FLOAT"]

class Channel:
    """
    Channel defines the type and spatial layout of a channel.
    *type* is a :class:`PixelType`.
    *xSampling* is the number of X-axis pixels between samples.
    *ySampling* is the number of Y-axis pixels between samples.

    .. doctest::
    
       >>> import Imath
       >>> print Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT), 4, 4)
       FLOAT (4, 4)
    """

    def __init__(self, type = PixelType(PixelType.HALF), xSampling = 1, ySampling = 1):
        self.type = type
        self.xSampling = xSampling
        self.ySampling = ySampling
    def __repr__(self):
        return repr(self.type) + " " + repr((self.xSampling, self.ySampling))
    def __eq__(self, other):
        return (self.type, self.xSampling, self.ySampling) == (other.type, other.xSampling, other.ySampling)

class PreviewImage:
    """
    .. index:: RGBA, thumbnail, preview, JPEG, PIL, Python Imaging Library

    PreviewImage is a small preview image, intended as a thumbnail version of the full image.
    The image has size (*width*, *height*) and 8-bit pixel values are
    given by string *pixels* in RGBA order from top-left to bottom-right.

    For example, to create a preview image from a JPEG file using the popular 
    `Python Imaging Library <http://www.pythonware.com/library/pil/handbook/index.htm>`_:

    .. doctest::
    
       >>> import Image
       >>> import Imath
       >>> im = Image.open("lena.jpg").resize((100, 100)).convert("RGBA")
       >>> print Imath.PreviewImage(im.size[0], im.size[1], im.tostring())
       <Imath.PreviewImage instance 100x100>
    """
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels
    def __repr__(self):
        return "<Imath.PreviewImage instance %dx%d>" % (self.width, self.height)

class LevelMode(Enumerated):
    ONE_LEVEL = 0
    MIPMAP_LEVELS = 1
    RIPMAP_LEVELS = 2
    names = ["ONE_LEVEL", "MIPMAP_LEVELS", "RIPMAP_LEVELS"]

class LevelRoundingMode(Enumerated):
    ROUND_DOWN = 0
    ROUND_UP = 1
    names = ["ROUND_DOWN", "ROUND_UP"]

class TileDescription:
    def __init__(self, xs = 32, ys = 32, m = LevelMode(LevelMode.ONE_LEVEL), r =LevelRoundingMode(LevelRoundingMode.ROUND_DOWN)):
        self.xSize = xs
        self.ySize = ys
        self.mode = m
        self.roundingMode = r
    def __repr__(self):
        return "<Imath.TileDescription instance %dx%d %s %s>" % (self.xSize, self.ySize, repr(self.mode), repr(self.roundingMode))
