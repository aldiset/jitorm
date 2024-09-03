import os
import sys
import distutils.sysconfig

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig


class BuildExt(build_ext_orig):
    def build_extensions(self):
        if sys.platform == "win32" and self.compiler.compiler_type == "msvc":
            # Use /MT flag for MSVC
            for ext in self.extensions:
                ext.extra_compile_args = ['/MT']
        super().build_extensions()

def get_python_include_dirs():
    if sys.platform == "win32":
        return [os.path.join(sys.prefix, 'include')]
    return [distutils.sysconfig.get_python_inc()]

def get_python_lib_dirs():
    if sys.platform == "win32":
        return [os.path.join(sys.prefix, 'libs')]
    return [distutils.sysconfig.get_config_var('LIBDIR')]

extension = Extension(
    'jit_wrapper',
    sources=['mapping.c'],
    include_dirs=get_python_include_dirs(),
    library_dirs=get_python_lib_dirs(),
    extra_compile_args=['-std=c99'] if sys.platform != "win32" else None
)

setup(
    name='jit_wrapper',
    version='1.0',
    ext_modules=[extension],
    cmdclass={'build_ext': BuildExt}
)
