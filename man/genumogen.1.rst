=========
genumogen
=========

---------------------------
generate a GLib enumeration
---------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2014 Eric Le Bihan
:Manual section: 1

SYNOPSIS
========

  genumogen [OPTIONS] <enum> <value> [<value>, ...]

DESCRIPTION
===========

  `genumogen` generates source code for a GLib enumeration, as well of its
  gtk-doc.

  The generated code is written to standard output.

OPTIONS
=======

  --version    show the program version and exit

EXAMPLES
========

  Generate source code for enumeration FooColorMode with values "rgb" and
  "yuv"::

    $ genumogen FooColorMode rgb yuv

.. vim: ft=rst
