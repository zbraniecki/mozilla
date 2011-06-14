#!/usr/bin/env python

from distutils.core import setup

setup(name='mozilla',
      version='1.0',
      description='Python mozilla library',
      author='Zbigniew Braniecki',
      author_email='zbigniew@braniecki.net',
      url='https://github.com/zbraniecki/mozilla',
      packages=['mozilla.format.dtd', 'mozilla.format.properties'],
     )

