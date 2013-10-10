===========
gobjectogen
===========

----------------------------------
generate GObject based source code
----------------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2013 Eric Le Bihan
:Manual section: 1

SYNOPSIS
========

  gobjectogen [OPTIONS] <name>

DESCRIPTION
===========

  `gobjectogen` generates source code for programs using the GObject type
  system, such as classes and interfaces. It produces one file for the C code
  and one for the header file. The *name* of the entity to be generated must
  be written in camel case: for example FooLoader.

  By default, the program generates a subclass of GObject. The parent class
  can be set using the *--parent* option. If *--abstract* is used, an
  abstract class will be generated. If *--interface* is used, an interface
  will be generated (an interface is an non-instanciable classed type).

  Other command line options are available to include the default property
  getter and setter, as well as private members or implemented interface.

OPTIONS
=======

  -o DIR, --output DIR          set output directory
  -N NAME, --namespace NAME     set namespace
  -P PARENT, --parent PARENT    set parent class
  -A, --abstract                generate an abstract class
  -F, --interface               generate an interface
  -I IFACE, --implements IFACE  set implemented interface
  -p, --private                 include structure to hold private members
  -d, --dispose                 include dispose method
  -f, --finalize                include finalize method
  -g, --propget                 include method to get properties
  -s, --propset                 include method to set properties

EXAMPLES
========

  Generate source code for simple class FooBarFrobnicator::

    $ gobjectogen -N FooBar FooBarFrobnicator

  Generate source code for complex class FooBarFrobnicator, which subclasses
  FooBaz, implements GooGlopable and has private members with accessors::

    $ gobjectogen -P FooBaz -I GooGlopable -gspdf FooFrobnicator

.. vim: ft=rst
