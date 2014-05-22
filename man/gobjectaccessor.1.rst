===============
gobjectaccessor
===============

--------------------------------
generate accessors for a GObject
--------------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2014 Eric Le Bihan
:Manual section: 1

SYNOPSIS
========

  gobjectaccessor [OPTIONS] <class> <property> <type>

DESCRIPTION
===========

  `gobjectacessor` generates source code for accessing a property of a
  GObject.

  By default, the program generates the source code of the accessors. If the
  option *--mode* is set to 'header', then the prototype of the functions are
  generated.

  The generated code is written to standard output.

OPTIONS
=======

  -B, --boxed                   generate code for GBoxed instead of GObject
  -M MODE, --mode MODE          set generation mode ('code', 'header')
  -N NAME, --namespace NAME     set namespace

EXAMPLES
========

  Generate source code for accessing the property "name" of class "FooBar"::

    $ gobjectaccessor FooBar name 'gchar*'

  Generate header code for accessing the property 'is-connected' of boxed type
  FooInfo::

    $ gobjectaccessor --boxed --mode=header FooInfo is-connected gboolean

.. vim: ft=rst
