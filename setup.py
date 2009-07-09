from distutils.core import setup
from distutils.extension import Extension
from distutils.command.build_py import build_py as _build_py

from os import system

from distutils.core import setup, Extension
setup(name='OpenEXR',
  author = 'James Bowman',
  author_email = 'jamesb@excamera.com',
  url = 'http://excamera.com/articles/26/openexr.html',
  version='1.0.2',
  data_files=['test-exr.py'],
  ext_modules=[ 
    Extension('OpenEXR',
              ['OpenEXR.cpp'],
              include_dirs=['/usr/include/OpenEXR', '/usr/local/include/OpenEXR'],
              library_dirs=['/usr/local/lib'],
              libraries=['Iex', 'Half', 'Imath', 'IlmImf', 'z'],
              extra_compile_args=['-g'])
  ],
  py_modules=['Imath'],
  # scripts=['test-exr.py']
)
