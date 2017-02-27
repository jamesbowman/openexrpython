from __future__ import print_function
import sys
import unittest
import random
from array import array

if sys.version_info[0] < 3:
    class ArrayProxy(array):
        def tobytes(self):
            return self.tostring()
    array = ArrayProxy

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

import Imath
import OpenEXR

class TestDirected(unittest.TestCase):

    def setUp(self):
        self.FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
        self.UINT = Imath.PixelType(Imath.PixelType.UINT)
        self.HALF = Imath.PixelType(Imath.PixelType.HALF)

    def load_red(self, filename):
        oexr = OpenEXR.InputFile(filename)
        return oexr.channel('R')

    def test_enumerants(self):
        self.assertEqual(Imath.LevelMode("ONE_LEVEL").v, Imath.LevelMode(Imath.LevelMode.ONE_LEVEL).v)
        self.assertEqual(Imath.LevelMode("MIPMAP_LEVELS").v, Imath.LevelMode(Imath.LevelMode.MIPMAP_LEVELS).v)
        self.assertEqual(Imath.LevelMode("RIPMAP_LEVELS").v, Imath.LevelMode(Imath.LevelMode.RIPMAP_LEVELS).v)

    def test_write_chunk(self):
        """ Write the pixels to two images, first as a single call,
        then as multiple calls.  Verify that the images are identical.
        """
        for w,h,step in [(100, 10, 1), (64,48,6), (1, 100, 2), (640, 480, 4)]:
            data = array('f', [ random.random() for x in range(w * h) ]).tobytes()

            hdr = OpenEXR.Header(w,h)
            x = OpenEXR.OutputFile("out0.exr", hdr)
            x.writePixels({'R': data, 'G': data, 'B': data})
            x.close()

            hdr = OpenEXR.Header(w,h)
            x = OpenEXR.OutputFile("out1.exr", hdr)
            for y in range(0, h, step):
                subdata = data[y * w * 4:(y+step) * w * 4]
                x.writePixels({'R': subdata, 'G': subdata, 'B': subdata}, step)
            x.close()

            oexr0 = self.load_red("out0.exr")
            oexr1 = self.load_red("out1.exr")
            self.assertTrue(oexr0 == oexr1)

    def test_write_mchannels(self):
        """
        Write N arbitrarily named channels.
        """
        hdr = OpenEXR.Header(100, 100)
        for chans in [ set("a"), set(['foo', 'bar']), set("abcdefghijklmnopqstuvwxyz") ]:
            hdr['channels'] = dict([(nm, Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT))) for nm in chans])
            x = OpenEXR.OutputFile("out0.exr", hdr)
            data = array('f', [0] * (100 * 100)).tobytes()
            x.writePixels(dict([(nm, data) for nm in chans]))
            x.close()
            self.assertEqual(set(OpenEXR.InputFile('out0.exr').header()['channels']), chans)

    def test_fail(self):
        self.assertRaises(IOError, lambda: OpenEXR.InputFile("non-existent"))
        hdr = OpenEXR.Header(640, 480)
        self.assertRaises(IOError, lambda: OpenEXR.OutputFile("/forbidden", hdr))

    def test_invalid_pt(self):
        f = OpenEXR.InputFile("GoldenGate.exr")
        FLOAT = Imath.PixelType.FLOAT
        self.assertRaises(TypeError, lambda: f.channel('R',FLOAT))
        
    def xtest_multiView(self):
        h = OpenEXR.Header(640, 480)
        for views in [[], ['single'], ['left', 'right'], list("abcdefghijklmnopqrstuvwxyz")]:
            h['multiView'] = views
            x = OpenEXR.OutputFile("out0.exr", h)
            x.close()
            self.assertEqual(OpenEXR.InputFile('out0.exr').header()['multiView'], views)

    def test_channel_channels(self):
        """ Check that the channel method and channels method return the same data """
        oexr = OpenEXR.InputFile("GoldenGate.exr")
        cl = sorted(oexr.header()['channels'].keys())
        a = [oexr.channel(c) for c in cl]
        b = oexr.channels(cl)
        self.assertEqual(a, b)

    def test_one(self):
        oexr = OpenEXR.InputFile("GoldenGate.exr")
        #for k,v in sorted(oexr.header().items()):
        #  print "%20s: %s" % (k, v)
        first_header = oexr.header()

        default_size = len(oexr.channel('R'))
        half_size = len(oexr.channel('R', Imath.PixelType(Imath.PixelType.HALF)))
        float_size = len(oexr.channel('R', Imath.PixelType(Imath.PixelType.FLOAT)))
        uint_size = len(oexr.channel('R', Imath.PixelType(Imath.PixelType.UINT)))

        self.assertTrue(default_size in [ half_size, float_size, uint_size])
        self.assertTrue(float_size == uint_size)
        self.assertTrue((float_size / 2) == half_size)

        self.assertTrue(len(oexr.channel('R', pixel_type = self.FLOAT, scanLine1 = 10, scanLine2 = 10)) == (4 * (first_header['dataWindow'].max.x + 1)))

        data = b" " * (4 * 100 * 100)
        h = OpenEXR.Header(100,100)
        x = OpenEXR.OutputFile("out.exr", h)
        x.writePixels({'R': data, 'G': data, 'B': data})
        x.close()

    def test_types(self):
        for original in [ [0,0,0], list(range(10)), list(range(100,200,3)) ]:
            for code,t in [ ('I', self.UINT), ('f', self.FLOAT) ]:
                data = array(code, original).tobytes()
                hdr = OpenEXR.Header(len(original), 1)
                hdr['channels'] = {'L': Imath.Channel(t)}

                x = OpenEXR.OutputFile("out.exr", hdr)
                x.writePixels({'L': data})
                x.close()

                xin = OpenEXR.InputFile("out.exr")
                # Implicit type
                self.assertTrue(array(code, xin.channel('L')).tolist() == original)
                # Explicit type
                self.assertTrue(array(code, xin.channel('L', t)).tolist() == original)
                # Explicit type as kwarg
                self.assertTrue(array(code, xin.channel('L', pixel_type = t)).tolist() == original)

    def test_conversion(self):
        """ Write an image as UINT, read as FLOAT.  And the reverse. """
        codemap = { 'f': self.FLOAT, 'I': self.UINT }
        original = [0, 1, 33, 79218]
        for frm_code,to_code in [ ('f','I'), ('I','f') ]:
            hdr = OpenEXR.Header(len(original), 1)
            hdr['channels'] = {'L': Imath.Channel(codemap[frm_code])}
            x = OpenEXR.OutputFile("out.exr", hdr)
            x.writePixels({'L': array(frm_code, original).tobytes()})
            x.close()

            xin = OpenEXR.InputFile("out.exr")
            self.assertEqual(array(to_code, xin.channel('L', codemap[to_code])).tolist(), original)

    def test_leak(self):
        hdr = OpenEXR.Header(10, 10)
        data = array('f', [ 0.1 ] * (10 * 10)).tobytes()
        for i in range(1000):
            x = OpenEXR.OutputFile("out.exr", hdr)
            x.writePixels({'R': data, 'G': data, 'B': data})
            x.close()
        return

        for i in range(1000):
            oexr = OpenEXR.InputFile("out.exr")
            h = oexr.header()

    def test_timecode_read(self):
        h = OpenEXR.InputFile("timecode.exr").header()
        a = h['keyCode']
        self.assertEqual(a.filmMfcCode,             2)
        self.assertEqual(a.filmType,                19)
        self.assertEqual(a.prefix,                  451681)
        self.assertEqual(a.count,                   9579)
        self.assertEqual(a.perfOffset,              51)
        self.assertEqual(a.perfsPerFrame,           4)
        self.assertEqual(a.perfsPerCount,           64)
        a = h['timeCode']
        self.assertEqual(a.hours,                   11)
        self.assertEqual(a.minutes,                 44)
        self.assertEqual(a.seconds,                 13)
        self.assertEqual(a.frame,                   7)
        self.assertEqual(a.dropFrame,               0)
        self.assertEqual(a.colorFrame,              0)
        self.assertEqual(a.fieldPhase,              0)
        self.assertEqual(a.bgf0,                    0)
        self.assertEqual(a.bgf1,                    0)
        self.assertEqual(a.bgf2,                    0)

    def test_code_loopback(self):
        """ Verify timeCode and keyCode field transit """
        data = b" " * (4 * 100 * 100)
        h = OpenEXR.Header(100,100)

        timecodes = [
            Imath.TimeCode(1, 2, 3, 4, 0, 0, 0, 0, 0, 0),
            Imath.TimeCode(1, 2, 3, 4, 1, 0, 0, 0, 0, 0),
            Imath.TimeCode(1, 2, 3, 4, 0, 1, 0, 0, 0, 0),
            Imath.TimeCode(1, 2, 3, 4, 0, 0, 1, 0, 0, 0),
            Imath.TimeCode(1, 2, 3, 4, 0, 0, 0, 1, 0, 0),
            Imath.TimeCode(1, 2, 3, 4, 0, 0, 0, 0, 1, 0),
            Imath.TimeCode(1, 2, 3, 4, 0, 0, 0, 0, 0, 1),
            Imath.TimeCode(1, 2, 3, 4, 1, 1, 1, 1, 1, 1),
        ]
        keycode = Imath.KeyCode(1, 2, 3, 4, 5, 6, 60)
        for timecode in timecodes:
            h['keyCode'] = keycode
            h['timeCode'] = timecode
            x = OpenEXR.OutputFile("out2.exr", h)
            x.writePixels({'R': data, 'G': data, 'B': data})
            x.close()
            h = OpenEXR.InputFile("out2.exr").header()
            self.assertEqual(h['keyCode'], keycode)
            self.assertEqual(h['timeCode'], timecode)

    def xtest_fileobject(self):
        f = StringIO()
        (w, h) = (640, 480)
        data = array('f', [0 for _ in range(w * h)]).tobytes()
        hdr = OpenEXR.Header(w,h)
        print(type(f), f)
        x = OpenEXR.OutputFile(f, hdr)
        x.writePixels({'R': data, 'G': data, 'B': data})
        x.close()
        f.seek(0)
        self.assertEqual(hdr, OpenEXR.InputFile(f).header())

    def test_write_buffer_object(self):
        (w, h) = (640, 480)
        a = array('f', [(i % w)/float(w) for i in range(w * h)])
        data = bytearray(a.tobytes())
        hdr = OpenEXR.Header(w,h)
        x = OpenEXR.OutputFile("out3.exr", hdr)
        x.writePixels({'R': data, 'G': data, 'B': data})
        x.close()
        r = self.load_red("out3.exr")
        self.assertTrue(r == data)

if __name__ == '__main__':
    if 1:
        unittest.main()
    else:
        suite = unittest.TestSuite()

        # Not working
        # suite.addTest(TestDirected('test_fileobject'))

        if 1:
            suite.addTest(TestDirected('test_enumerants'))
            suite.addTest(TestDirected('test_conversion'))
            suite.addTest(TestDirected('test_fail'))
            suite.addTest(TestDirected('test_one'))
            suite.addTest(TestDirected('test_channel_channels'))
            suite.addTest(TestDirected('test_types'))
            suite.addTest(TestDirected('test_leak'))
            suite.addTest(TestDirected('test_invalid_pt'))
            suite.addTest(TestDirected('test_write_mchannels'))
            suite.addTest(TestDirected('test_write_chunk'))
        unittest.TextTestRunner(verbosity=2).run(suite)
