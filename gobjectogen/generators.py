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

import os
import re
import pystache
from . import templates
import gettext
from gettext import gettext as _

def camel_to_upper(string):
    crumbs = re.findall(r'[A-Z][^A-Z]*', string)
    return '_'.join([x.upper() for x in crumbs])

def camel_to_lower(string):
    crumbs = re.findall(r'[A-Z][^A-Z]*', string)
    return '_'.join([x.lower() for x in crumbs])

def split_class_name(klass_name):
    return re.split(r'(^[A-Z][^A-Z]*)', klass_name, 1)[1:]

def write_file(filename, contents):
    with open(filename, 'w') as output:
        output.write(contents)
    print(_("Wrote %s") % filename)

CLASS_HAS_PRIVATE = 1 << 0
CLASS_HAS_PROPGET = 1 << 1
CLASS_HAS_PROPSET = 1 << 2
CLASS_HAS_DISPOSE = 1 << 3
CLASS_HAS_FINALIZE = 1 << 4
CLASS_IS_ABSTRACT = 1 << 5

class ClassGenerator:
    '''Generates source code for objects.

    :param name: name of the class
    :type  name: str

    A class is a instanciabled classed-type.
    '''

    parent = None
    namespace = None
    interfaces = []
    flags = 0

    def __init__(self, name):
        self._klass_name = name
        self._values = {}
        self._header = templates.TEMPLATE_CLASS_HEADER
        self._code = templates.TEMPLATE_CLASS_CODE

    def generate(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.update_values()
        self.generate_header(directory)
        self.generate_code(directory)

    def update_values(self):
        if self.parent == None:
            self.parent = 'GObject'
        if self.namespace == None:
            self.namespace, object_camel = split_class_name(self._klass_name)
        else:
            object_camel = self._klass_name.replace(self.namespace, '')

        parent_ns_upper, parent_object_upper = split_class_name(self.parent)

        implemented_ifaces = []
        ifaces = []
        for iface in self.interfaces:
            ns, name = split_class_name(iface)
            values = {
                'iface_lower': camel_to_lower(iface),
                'iface_camel': iface,
                'iface_ns_upper': camel_to_upper(ns),
                'iface_name_upper': camel_to_upper(name),
                 }
            implemented_ifaces.append(templates.TEMPLATE_IFACE_DECL % values)
            ifaces.append(values)

        values = {
                'ns_upper': camel_to_upper(self.namespace),
                'object_upper': camel_to_upper(object_camel),
                'class_camel': self._klass_name,
                'class_lower': camel_to_lower(self._klass_name),
                'parent_camel' : self.parent,
                'parent_ns_upper': camel_to_upper(parent_ns_upper),
                'parent_object_upper': camel_to_upper(parent_object_upper),
                'header_guard': camel_to_upper(self._klass_name) + '_H',
                'filename': camel_to_lower(self._klass_name).replace('_', '-'),
                'define_type': '',
                'has_private': self.flags & CLASS_HAS_PRIVATE,
                'has_propset': self.flags & CLASS_HAS_PROPSET,
                'has_propget': self.flags & CLASS_HAS_PROPGET,
                'has_dispose': self.flags & CLASS_HAS_DISPOSE,
                'has_finalize': self.flags & CLASS_HAS_FINALIZE,
                'has_class_init': self.flags != 0,
                'is_abstract': self.flags & CLASS_IS_ABSTRACT,
                'implements_iface': len(self.interfaces) != 0,
                'implemented_ifaces': ',\n'.join(implemented_ifaces),
                'ifaces': ifaces,
                }
        self._values.update(values)

    def generate_header(self, directory):
        filename = os.path.join(directory, self._values['filename'])
        filename += '.h'

        contents = pystache.render(self._header, self._values)
        write_file(filename, contents)

    def generate_code(self, directory):
        filename = os.path.join(directory, self._values['filename'])
        filename += '.c'

        contents = pystache.render(self._code, self._values)
        write_file(filename, contents)

class InterfaceGenerator(ClassGenerator):
    '''Generates source code for interfaces.

    :param name: name of the class
    :type  name: str

    An interface is a non-instanciable classed type.
    '''
    def __init__(self, name):
        ClassGenerator.__init__(self, name)
        self._header = templates.TEMPLATE_IFACE_HEADER
        self._code = templates.TEMPLATE_IFACE_CODE

    def update_values(self):
        ClassGenerator.update_values(self)
        self._values['iface_camel'] = self._values['class_camel']
        self._values['iface_lower'] = self._values['class_lower']
        self._values['iface_upper'] = self._values['object_upper']

# vim: ts=4 sw=4 sts=4 et ai
