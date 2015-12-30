#!/usr/bin/env python3
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
#

from setuptools import setup, find_packages
from disthelpers import extract_messages, init_catalog, update_catalog
from disthelpers import build, build_catalog, build_man, build_html
from glob import glob
from gobjectogen import __version__
import fnmatch
import os


def collect_data_files(dst_dir, src_dir):
    data_files = []
    for root, directory, filenames in os.walk(src_dir):
        for filename in fnmatch.filter(filenames, '*.mustache'):
            src = os.path.join(root, filename)
            dst = root.replace(src_dir, dst_dir)
            data_files.append((dst, [src]))
    return data_files

setup(name='gobjectogen',
      version=__version__,
      description='GObject source code generator',
      long_description='''
      This program generates source code for programs using the GObject type
      system, such as classes or interfaces.
      ''',
      license='GPLv3',
      url='https://github.com/elebihan/gobjectogen/',
      platforms=['Any'],
      classifiers=('Programming Language :: Python :: 3',
                   'Intended Audience :: Developers',
                   'Natural Language :: English'
                   'License :: OSI Approved :: GNU General Public License (GPL)',),
      keywords=['gobject', 'code generator'],
      install_requires=['pystache >= 0.5', 'docutils >=0.11'],
      packages=find_packages(),
      data_files=[
          ('share/zsh/site-functions', glob('shell-completion/zsh/_*')),
      ] + collect_data_files('share/gobjectogen', 'data'),
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'genumogen = gobjectogen.cli:genumogen',
              'gobjectaccessor = gobjectogen.cli:gobjectaccessor',
              'gobjectogen = gobjectogen.cli:gobjectogen',
          ],
      },
      author='Eric Le Bihan',
      author_email='eric.le.bihan.dev@free.fr',
      cmdclass={'build': build,
                'build_man': build_man,
                'build_html': build_html,
                'extract_messages': extract_messages,
                'init_catalog': init_catalog,
                'update_catalog': update_catalog,
                'build_catalog': build_catalog})

# vim: ts=4 sts=4 sw=4 sta et ai
