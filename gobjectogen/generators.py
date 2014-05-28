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
from gettext import gettext as _
from datetime import datetime

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
    author = None
    description = None
    license = None
    interfaces = []
    errors = []
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
        if self.parent is None:
            self.parent = 'GObject'
        if self.namespace is None:
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

        if self.license is None:
            self.license = 'Insert license text here'

        lines = map(lambda l: " * {}".format(l), self.license.split('\n'))

        values = {
            'ns_upper': camel_to_upper(self.namespace),
            'object_upper': camel_to_upper(object_camel),
            'class_camel': self._klass_name,
            'class_upper': camel_to_upper(self._klass_name),
            'class_lower': camel_to_lower(self._klass_name),
            'parent_camel': self.parent,
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
            'description': self.description,
            'author': self.author,
            'year': datetime.today().year,
            'license': '\n'.join(lines),
        }
        self._values.update(values)

        if self.errors:
            errors = []
            error_type = "{0}Error".format(self._klass_name)
            for error in self.errors:
                name = "{0}_ERROR_{1}".format(camel_to_upper(self._klass_name),
                                              error.upper().replace('-', '_'))
                errors.append({'error': name})

            values = {
                'has_errors': True,
                'error_type': error_type,
                'errors': errors
            }
            self._values.update(values)

    def generate_header(self, directory):
        filename = os.path.join(directory, self._values['filename']) + '.h'
        self._render_template(self._header, filename)

    def generate_code(self, directory):
        filename = os.path.join(directory, self._values['filename']) + '.c'
        self._render_template(self._code, filename)

    def _render_template(self, text, filename):
        renderer = pystache.Renderer(escape=lambda u: u)
        contents = renderer.render(text, self._values)
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

class BoxedGenerator(ClassGenerator):
    '''Generates source code for boxed types.

    :param name: name of the boxed type
    :type  name: str

    A boxed type is a wrapper around an opaque C structure.
    '''
    def __init__(self, name):
        ClassGenerator.__init__(self, name)
        self._header = templates.TEMPLATE_BOXED_HEADER
        self._code = templates.TEMPLATE_BOXED_CODE

    def update_values(self):
        ClassGenerator.update_values(self)
        self._values['boxed_camel'] = self._values['class_camel']
        self._values['boxed_lower'] = self._values['class_lower']
        self._values['boxed_upper'] = self._values['object_upper']

class AccessorGenerator:
    '''Generates source code for accessing a property of a GObject.

    :param klass_name: name of the GObject class
    :type klass_name: str

    :param prop_name: name of the property to access.
    :type prop_name: str

    :param prop_type: type of the property to access.
    :type prop_type: str
    '''

    namespace = None
    boxed = False

    MODE_HEADER, MODE_CODE = range(2)

    def __init__(self, klass_name, prop_name, prop_type):
        self._klass_name = klass_name

        prop_name = prop_name.replace('-', '_')

        setter = "{}_set_{}".format(camel_to_lower(klass_name), prop_name)
        getter = "{}_get_{}".format(camel_to_lower(klass_name), prop_name)

        if prop_type == 'gchar*':
            prop_type = 'const gchar*'
        if prop_type[-1] == '*':
            prop_assert = "g_return_if_fail({} != NULL);".format(prop_name)
            prop_assert_ret = 'NULL'
        else:
            if prop_type == 'gboolean':
                prop_assert_ret = 'FALSE'
            else:
                prop_assert_ret = '0'
            prop_assert = ''

        self._values = {
            'class_camel': klass_name,
            'class_upper': camel_to_upper(klass_name),
            'setter': setter,
            'getter': getter,
            'prop_name': prop_name,
            'prop_type': prop_type,
            'prop_assert': prop_assert,
            'prop_assert_ret': prop_assert_ret,
        }

    def generate(self, mode=MODE_CODE):
        '''Generates accessor source code.

        :param mode: mode of generation.
        :type mode:
        '''
        if self.namespace is None:
            namespace, object_camel = split_class_name(self._klass_name)
        else:
            object_camel = self._klass_name.replace(self.namespace, '')
            namespace = self.namespace

        values = {
            'ns_upper': camel_to_upper(namespace),
            'object_upper': camel_to_upper(object_camel),
            'is_boxed': self.boxed
        }
        self._values.update(values)

        if mode == AccessorGenerator.MODE_HEADER:
            text = templates.TEMPLATE_ACCESSORS_HEADER
        else:
            text = templates.TEMPLATE_ACCESSORS_CODE

        renderer = pystache.Renderer(escape=lambda u: u)
        contents = renderer.render(text, self._values)
        print(contents)

class EnumGenerator:
    '''Generates source code for a GLib enumeration.

    :param name: name of the enumeration
    :type name: str

    :param values: list of values
    :type values: list of str
    '''

    def __init__(self, name, values):
        self._enum_name = name
        self._enum_values = values

    def generate(self):
        enum_values = []
        for value in self._enum_values:
            newval = "{0}_{1}".format(camel_to_upper(self._enum_name),
                                      value.upper().replace('-', '_'))
            enum_values.append({'value': newval})
        values = {
            'enum_name': self._enum_name,
            'enum_values': enum_values,
        }
        text = templates.TEMPLATE_ENUMS_HEADER
        renderer = pystache.Renderer(escape=lambda u: u)
        contents = renderer.render(text, values)
        print(contents)

# vim: ts=4 sw=4 sts=4 et ai
