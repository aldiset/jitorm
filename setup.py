import os
import sys

from distutils.sysconfig import get_python_inc, get_config_var
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as BuildExtOrig


class BuildExt(BuildExtOrig):
    def build_extensions(self):
        if sys.platform == "win32" and self.compiler.compiler_type == "msvc":
            for ext in self.extensions:
                ext.extra_compile_args = ['/MT']
        super().build_extensions()

def get_python_include_dirs():
    return [os.path.join(sys.prefix, 'include')] if sys.platform == "win32" else [get_python_inc()]

def get_python_lib_dirs():
    return [os.path.join(sys.prefix, 'libs')] if sys.platform == "win32" else [get_config_var('LIBDIR')]

extension = Extension(
    'jit_wrapper',
    sources=['mapping.c'],
    include_dirs=get_python_include_dirs(),
    library_dirs=get_python_lib_dirs(),
    extra_compile_args=['-std=c99'] if sys.platform != "win32" else []
)

setup(
    name='jit_wrapper',
    version='1.0',
    ext_modules=[extension],
    cmdclass={'build_ext': BuildExt}
)
