#include <ImfRgba.h>
#include <ImfRgbaFile.h>

using namespace Imf;

void
writeRgba1 (const char fileName[],
            const Rgba *pixels,
            int width,
            int height)
{
    RgbaOutputFile file (fileName, width, height, WRITE_RGBA);
    file.setFrameBuffer (pixels, 1, width);
    file.writePixels (height);
}

main() {
    Rgba *pixels = new Rgba[1980 * 1080];
    int i;

    for (i = 0; i < 10; i++)
        writeRgba1("/dev/null", pixels, 1980, 1080);
}
