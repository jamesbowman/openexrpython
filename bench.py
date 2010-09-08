import OpenEXR
import Imath

(w, h) = (1920, 1080)

data = ".." * w * h

for i in range(10):
    hdr = OpenEXR.Header(w, h)
    chan = Imath.Channel(Imath.PixelType(OpenEXR.HALF))
    hdr['channels'] = {'R' : chan, 'G' : chan, 'B' : chan, 'A' : chan}
    x = OpenEXR.OutputFile("/dev/null", hdr)
    x.writePixels({'R': data, 'G': data, 'B': data, 'A' : data})
    x.close()
