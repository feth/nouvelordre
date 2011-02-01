Nouvel Ordre
============

A tool for *reordering import statements* inside Python code blocks.

This project lives on github:

* github html page: http://feth.github.com/nouvelordre/
* github classic page: https://github.com/feth/nouvelordre
* repository::

  $ git clone git://github.com/feth/nouvelordre.git

Getting started
---------------

Common usage
~~~~~~~~~~~~
**'reorder'** is an executable script::

  $ nouvelordre.py --infile mymodule.py --outfile rewritten.py
  $ nouvelordre.py < mymodule.py > rewritten.py

You may want to rewrite all files in a directory, say '/home/toto/project'::

  $ for file in $(find '/home/toto/project') ; do reorder -i $file -o $file ; done
  $ <run your test suite!>
  $ git diff

**of course, if you run the above, you are using version control so you can check the diff and revert modifications in case of trouble**

Installation
------------
The installation procedure is not very good for the moment but should work.

From source::

  $ python setup.py install

From the internet (Pypi - http://pypi.python.org )::

  $ pip install nouvelordre

As a side note, I suggest installing in a *virtualenv* -this means running the following before installing as above, therefore not polluting your system::

  $ virtualenv nouvelordre
  $ cd nouvelordre
  $ source ./bin/activate

Options
~~~~~~~
options::

  --infile INFILE, -i INFILE            a Python source file, defaults to standard input
  --outfile OUTFILE, -o OUTFILE         output, defaults to standard output
  --dump, -d                            in case of failure, keep processing data in files
  --version, -v                         prints version and exits

This means equivalent common usages can be::

Features
--------
* Blocks separated by anything (white line for instance) are considered separately.
* Statements inside a block are reordered
* Imports in one statement are reordered.
  Example::

    import sys, os

  becomes::

    import os
    import sys

  or::

    from module import b, a as f, c

  becomes::

    from module import a as f, b, c
* Tries and avoid damaging your precious Python work (see below, Disaster avoidance)

Limitations
-----------

* This script will only handle first level statements (ie. not indented statements).
* This script will not handle several "import module" for the same module in the same block.
* Some files are not compilables by ast.parse() (help appreciated).

Dependances
-----------

Compulsory
~~~~~~~~~~

* Python 2.6 at least (for ast)
* Python 2.7 or python-argparse

Recommended
~~~~~~~~~~~

* enthought's python-traits - provides type verification and may catch some bugs (absolutely compulsory if you intend to patch this software).

Exit codes
----------

* 0 if all is well.
* 129 if NotImplementedError (an import on the same line as another instruction, separated by ';').
* 130 if ast.parse was not able to compile the file.

Disaster avoidance
------------------

This software is not perfect and might kill your golden retriever or ruin your diploma but I have tried hard for this never to happen.

**'reorder'** performs 2 passes. Pass 1 is performed on the original input; pass 2 is performed on the result of pass 1.
If any error occurred during either pass, the program exits and leaves your files untouched.
If pass 1 and 2 would give a different result, the program exits and leaves your files untouched. This is not a 100% guarantee, but it ensures the file stays compilable and all optimizations were performed.

Just because I prefer my program to admit that it failed than to shred your beautiful Python source code.

