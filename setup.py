from distutils.core import setup
from distutils.extension import Extension
from distutils.command.build_py import build_py as _build_py
from distutils.sysconfig import get_config_var
from distutils.version import LooseVersion
import sys
import os
import platform

from distutils.core import setup, Extension

version = "1.3.2"
compiler_args = ['-g', '-DVERSION="%s"' % version]

if sys.platform == 'darwin':
    compiler_args.append('-std=c++14')
    if 'MACOSX_DEPLOYMENT_TARGET' not in os.environ:
        current_system = LooseVersion(platform.mac_ver()[0])
        python_target = LooseVersion(
            get_config_var('MACOSX_DEPLOYMENT_TARGET'))
        if python_target < '10.9' and current_system >= '10.9':
            os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.9'

            
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
              extra_compile_args=compiler_args)
  ],
  py_modules=['Imath'],
)
