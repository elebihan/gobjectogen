# -*- coding: utf-8 -*-
#
# gobjectogen - GObject generator
#
# Copyright (c) 2013 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
from disthelpers import build, build_trans, install_data
import sys

setup(name='gobjectogen',
      version='0.1.0',
      description='GObject source code generator',
      long_description='''
      This program generates source code for programs using the GObject type
      system, such as classes or interfaces.
      ''',
      license='GPLv3',
      url='https://github.com/elebihan/gobjectogen/',
      platforms=['Any'],
      keywords=['gobject', 'code generator'],
      install_requires=['pystache>=0.5'],
      packages=['gobjectogen'],
      scripts=['scripts/gobjectogen'],
      data_files=[('share/man/man1', ['data/gobjectogen.1'])],
      author='Eric Le Bihan',
      author_email='eric.le.bihan.dev@free.fr',
      cmdclass = {'build': build, 'build_trans': build_trans,
                  'install_data': install_data})

# vim: ts=4 sts=4 sw=4 sta et ai
