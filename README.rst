Nouvel Ordre
============

A tool for reordering import statements inside Python code blocks.

This project lives on github:

* github html page: http://feth.github.com/nouvelordre/
* github classic page: https://github.com/feth/nouvelordre
* repository::

  $ git clone git://github.com/feth/nouvelordre.git

Getting started
---------------
'reorder' is an executable script.

Options::

  --infile INFILE    a Python source file, defaults to standard input
  --outfile OUTFILE  output, defaults to standard output

This means equivalent common usages can be::

  $ nouvelordre.py --infile mymodule.py --outfile rewritten.py
  $ nouvelordre.py < mymodule.py > rewritten.py

Features
--------
* Blocks separated by anything (white line for instance) are considered separately.
* Statements inside a block are reordered
* Imports in one statement are reordered.
  Example::

    import sys, os

  becomes::

    import os, sys

  or::

    from module import b, a as f, c

  becomes::

    from module import a as f, b, c

Limitations
-----------

* This script will only handle first level statements.
* This script will not handle several "import module" for the same module in the same block.
* Some files are not compilables by ast.parse (help appreciated).

Dependances
-----------

Compulsory
~~~~~~~~~~

* Python 2.6 at least (for ast)
* Python 2.7 or python-argparse

Recommended
~~~~~~~~~~~

* enthought's python-traits - to avoid bug while coding this

Exit codes
----------
* 0 if all is well.
* 129 if NotImplementedError (an import on the same line as another instruction, separated by ';').
* 130 if ast.parse was not able to compile the file.

