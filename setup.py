__author__ = 'lucas'
import pytest

from distutils.core import setup

setup(
    name='captura',
    version='1.0',
    description='captura',
    author='Lucas',
    author_email='lffsantos@gmail.com',
    url='https://github.com/lffsantos/captura',
    packages=[
      'core',
      'core.db',
      'core.modules',
      'core.utils',
      'config',
      'core.tests.fixtures'
    ],
)