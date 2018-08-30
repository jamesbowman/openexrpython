from distutils.core import setup
from distutils.extension import Extension
from distutils.command.build_py import build_py as _build_py

from os import system

from distutils.core import setup, Extension

version = "1.3.1"
setup(name='OpenEXR',
  author = 'James Bowman',
  author_email = 'jamesb@excamera.com',
  url = 'http://www.excamera.com/sphinx/articles-openexr.html',
  description = "Python bindings for ILM's OpenEXR image file format",
  long_description = "Python bindings for ILM's OpenEXR image file format",
  version=version,
  ext_modules=[ 
    Extension('OpenEXR',
              ['OpenEXR.cpp'],
              include_dirs=['/usr/include/OpenEXR', '/usr/local/include/OpenEXR', '/opt/local/include/OpenEXR'],
              library_dirs=['/usr/local/lib', '/opt/local/lib'],
              libraries=['Iex', 'Half', 'Imath', 'IlmImf', 'z'],
              extra_compile_args=['-g', '-DVERSION="%s"' % version])
  ],
  py_modules=['Imath'],
)
