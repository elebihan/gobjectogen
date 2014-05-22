gobjectogen - GObject Source Code Generator
===========================================

`gobjectogen` generates source code for programs using the GObject type system,
such as classes or interfaces.

The generated code is not fully indented, so it is better to use `astyle` (>=
2.03) to format them::

  $ gobjectogen -N FooBar -I FooSerializable -I FooLoadable \
  -gsdfp FooBarFrobnicator \
  | cut -d ' ' -f2 \
  | xargs astyle \
  --style=linux \
  --indent=tab=8 \
  --max-code-length=80 \
  --align-pointer=name \
  --indent-preprocessor

Another tool is available for generating source/header code for accessing a
property of an object: `gobjectaccessor`.

.. vim: ft=rst
