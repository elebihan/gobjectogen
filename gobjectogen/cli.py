# -*- coding: utf-8 -*-
#
# gobjectogen - GObject generator
#
# Copyright (c) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
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

"""
   gobjectogen.cli
   ```````````````

   Provides command line interpeter helpers

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import argparse
from gobjectogen import __version__
from gobjectogen.generators import (
    AccessorGenerator, EnumGenerator, ClassGenerator, InterfaceGenerator,
    BoxedGenerator
)
from gobjectogen.generators import (
    CLASS_HAS_PRIVATE, CLASS_HAS_PROPGET, CLASS_HAS_PROPSET,
    CLASS_HAS_DISPOSE, CLASS_HAS_FINALIZE, CLASS_IS_ABSTRACT
)
from gettext import gettext as _


def genumogen():
    """
    Generate source code for a GLib enumeration, as well of its gtk-doc.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version=__version__)
    parser.add_argument('name',
                        metavar=_('NAME'),
                        help=_('name of the GObject class (in CamelCase)'))
    parser.add_argument('values',
                        nargs='+',
                        metavar=_('VALUE'),
                        help=_('value of the enumeration'))

    args = parser.parse_args()

    gen = EnumGenerator(args.name, args.values)
    gen.generate()


def gobjectaccessor():
    """
    Generate source code for accessing a property of a GObject.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version=__version__)
    parser.add_argument('class_name',
                        metavar=_('CLASS'),
                        help=_('name of the GObject class (in CamelCase)'))
    parser.add_argument('prop_name',
                        metavar=_('PROPERTY'),
                        help=_('name of the property'))
    parser.add_argument('prop_type',
                        metavar=_('TYPE'),
                        help=_('type of the property'))
    parser.add_argument('-B', '--boxed',
                        action='store_true',
                        help=_('generate code for GBoxed instead of GObject'))
    parser.add_argument('-M', '--mode',
                        choices=['code', 'header'],
                        default='code',
                        help=_('set generation mode'))
    parser.add_argument('-N', '--namespace',
                        metavar=_('NAME'),
                        help=_('set namespace'))

    args = parser.parse_args()

    modes = {
        'code': AccessorGenerator.MODE_CODE,
        'header': AccessorGenerator.MODE_HEADER,
    }

    gen = AccessorGenerator(args.class_name, args.prop_name, args.prop_type)
    gen.namespace = args.namespace
    gen.boxed = args.boxed
    gen.generate(modes[args.mode])


def configure_generator(gen, args):
    gen.parent = args.parent
    gen.namespace = args.namespace
    gen.interfaces = args.interfaces
    gen.errors = args.errors
    gen.author = args.author
    gen.description = args.description
    if args.private:
        gen.flags |= CLASS_HAS_PRIVATE
    if args.propget:
        gen.flags |= CLASS_HAS_PROPGET
    if args.propset:
        gen.flags |= CLASS_HAS_PROPSET
    if args.dispose:
        gen.flags |= CLASS_HAS_DISPOSE
    if args.finalize:
        gen.flags |= CLASS_HAS_FINALIZE
    if args.abstract:
        gen.flags |= CLASS_IS_ABSTRACT

    if args.license_file:
        with open(args.license_file) as f:
            gen.license = f.read()


def gobjectogen():
    """
    Generate source code for programs using the GObject type system, such as
    classes and interfaces.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version=__version__)
    parser.add_argument('name',
                        metavar=_('NAME'),
                        help=_('name of the GObject class (in CamelCase)'))
    parser.add_argument('-o', '--output',
                        metavar=_('DIRECTORY'),
                        default=os.getcwd(),
                        help=_('set output directory'))
    parser.add_argument('-N', '--namespace',
                        metavar=_('NAME'),
                        help=_('set namespace'))
    parser.add_argument('-P', '--parent',
                        help=_('set parent class'))
    parser.add_argument('-I', '--implements',
                        action='append',
                        dest='interfaces',
                        default=[],
                        metavar=_('INTERFACE'),
                        help=_('set implemented interface'))
    parser.add_argument('-A', '--abstract',
                        action='store_true',
                        default=False,
                        help=_('generate an abstract class'))
    parser.add_argument('-B', '--boxed',
                        action='store_true',
                        default=False,
                        help=_('generate a boxed type'))
    parser.add_argument('-F', '--interface',
                        action='store_true',
                        default=False,
                        help=_('generate an interface'))
    parser.add_argument('-E', '--error',
                        action='append',
                        dest='errors',
                        default=[],
                        metavar=_('NAME'),
                        help=_('add an error code'))
    parser.add_argument('-p', '--private',
                        action='store_true',
                        default=False,
                        help=_('include structure to hold private members'))
    parser.add_argument('-d', '--dispose',
                        action='store_true',
                        default=False,
                        help=_('include dispose method'))
    parser.add_argument('-f', '--finalize',
                        action='store_true',
                        default=False,
                        help=_('include finalize method'))
    parser.add_argument('-s', '--propset',
                        action='store_true',
                        default=False,
                        help=_('include method to set properties'))
    parser.add_argument('-g', '--propget',
                        action='store_true',
                        default=False,
                        help=_('include method to get properties'))
    parser.add_argument('-a', '--author',
                        metavar=_('NAME'),
                        default='Unknown',
                        help=_('set author of the program'))
    parser.add_argument('-t', '--description',
                        metavar=_('TEXT'),
                        default='Insert program description here',
                        help=_('set description of the program'))
    parser.add_argument('-l', '--license-file',
                        metavar=_('FILE'),
                        help=_('set path to license file'))
    args = parser.parse_args()

    if args.interface:
        gen = InterfaceGenerator(args.name)
    elif args.boxed:
        gen = BoxedGenerator(args.name)
    else:
        gen = ClassGenerator(args.name)
    configure_generator(gen, args)

    gen.generate(args.output)

# vim: ts=4 sw=4 sts=4 et ai
