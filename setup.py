from setuptools import setup, Extension

# Define the extension module
extension_mod = Extension('jit_wrapper', sources=['mapping.c'])

# Run the setup
setup(
    name='jit_wrapper',
    version='1.0',
    description='JIT Wrapper for ORM Mapping',
    ext_modules=[extension_mod],
)
