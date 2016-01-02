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

"""
   gobjectogen.templates
   `````````````````````

   GObject C header/source code templates management

   :copyright: (C) 2013 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
from .utils import get_data_dir


def get_default_templates_dir():
    """Return the path to the default templates directory"""
    return os.path.join(get_data_dir(), 'templates')


def read_template(basename):
    """Read contents of a template file from default directory.

    :param basename: name of the template file
    :type basename: string

    :return: the contents of the template file
    :rtype: str
    """
    filename = os.path.join(get_default_templates_dir(), basename)
    with open(filename) as f:
        return f.read()

TEMPLATE_IFACE_DECL = "G _IMPLEMENT_INTERFACE(%(iface_ns_upper)s_TYPE_%(iface_name_upper)s, %(iface_lower)s_iface_init)"

# vim: ts=4 sw=4 sts=4 et ai
