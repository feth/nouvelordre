#!/usr/bin/python
#coding: utf-8

"""
NouvelOrdre
© Feth Arezki - feth >AT< tuttu.info, 2011

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


from _ast import Import, ImportFrom
from ast import parse
from enthought.traits.api import Dict, Either, HasTraits, Int, List, Str, Tuple


class Block(HasTraits):
    """
    The base for code block
    """
    content = Str


class AnyBlock(Block):
    """
    Here lie the blocks that we consider raw and don't modify
    """

    def __init__(self, content):
        self.content = ''.join(content)


def spitfrom(module, data):
    """
    module: string
    data: list of duples: (name, asname) - asname may be None
    """
    lines = ['from %s import' % module]
    for index, (name, asname) in enumerate(data):
        if index:
            #not adding comma when index == 0
            lines[-1] += ','
        if asname:
            addition = ' %s as %s' % name, asname
        else:
            addition = ' %s' % name

        if len(lines[-1]) + len(addition) > 79:
            lines[-1] += '\\'
            lines.append('    ')
        lines[-1] += addition

    return '\n'.join(lines)



def nice_fromline(data):
    """
    Removes doubly imported names, sort names.
    """
    #remove doubles
    data = set(data)
    #sort
    data = list(data)
    data.sort()
    return data


def eval_continuation(line, open_par_nb):
    """
    Returns information whether the line continues
    """
    for char in line:
        if char == '(':
            open_par_nb += 1
        if char == ')':
            assert open_par_nb >= 1
            open_par_nb -= 1
    return open_par_nb, line.endswith('\\')


class ImportBlock(Block):
    """
    Code blocks consisting of imports are handled here.
    """

    importfroms = Dict(str, List(Tuple(str, Either(str, None))))
    imports = Dict(str, Either(str, None))
    startline = Int(default_value=-1)
    endline = Int()

    def add(self, statement, endline):
        """
        Add a statement to this block
        """
        assert self.followsme(statement)

        self._setstartline(statement)
        self.endline = endline

        if isinstance(statement, ImportFrom):
            module = statement.module
            self.importfroms.setdefault(module, [])
            for alias in statement.names:
                self.importfroms[module].append((alias.name, alias.asname))
        elif isinstance(statement, Import):
            for alias in statement.names:
                if alias.name in self.imports:
                    raise NotImplementedError(
                        "Can not handle several 'imports module' type statements"
                        "of the same module. Could, though, sorry."
                        )
                self.imports[alias.name] = alias.asname

    def followsme(self, statement):
        """
        Does the supplied statement follow this block?
        """
        if not self.importfroms:
            return True
        return statement.lineno == self.endline + 1

    def _setstartline(self, statement):
        startline = statement.lineno
        if self.startline <= 0:
            self.startline = startline
        else:
            self.startline = min(self.startline, startline)

    def __str__(self):
        return 'ImportBlock from line %d to line %d (%d imports)' % (
            self.startline, self.endline, len(self.imports)
            )

    def _pretty(self):
        for module, data in self.importfroms.iteritems():
            data = nice_fromline(data)
            yield spitfrom(module, data)
        for imp, asname in self.imports.iteritems():
            if asname:
                yield 'import %s as %s' % (imp, asname)
                continue
            yield 'import %s' % imp

    def _content(self):
        newblock = list(self._pretty())
        newblock.sort()
        return '%s\n' % '\n'.join(newblock)

    content = property(fget=_content)

class NewOrder(object):
    """
    Class handling your Python source code
    """

    def __init__(self, infile):
        """
        infile: a file descriptor like (must return lines when iterated over)
        """

        self.origlines =  list(infile)

        self.parsed = parse(''.join(self.origlines)).body

        self.firstlevels = []
        firstlevels_dict = {}
        for firstlevel in self.parsed:
            lineno = firstlevel.lineno
            registered = firstlevels_dict.setdefault(lineno, firstlevel)
            if  registered != firstlevel:
                raise NotImplementedError(
                    "Not handling several first level statements on the "
                    "same line (line %d of %s) -avoid semicolumns."
                    % (lineno, infile.name)
                    )
            self.firstlevels.append(firstlevel)

    def reorder(self, fdesc):
        """
        fdesc will be written upon (write())
        """
        for block in self.iter_blocks():
            fdesc.write(block.content)

    def iter_blocks(self):
        """
        Iterate over the recognized code blocks
        """
        last_handled = 0
        for block in self._iter_importblocks():
            if block.startline != last_handled + 1:
                yield AnyBlock(self.origlines[last_handled:block.startline - 1])
            yield block
            last_handled = block.endline
        yield AnyBlock(self.origlines[last_handled:])

    def _iter_importblocks(self):
        current_block = ImportBlock()

        for imp in self._iter_imports():

            if not current_block.followsme(imp):
                yield current_block
                current_block = ImportBlock()

            current_block.add(imp, self._statement_lastline(imp))

        yield current_block

    def _iter_imports(self):
        return iter(
            statement
            for statement in self.firstlevels
            if isinstance(statement, (ImportFrom, Import))
            )

    def _statement_lastline(self, statement):
        """
        text parsing
        """

        open_par_nb = 0
        startline = statement.lineno

        #- 1 is because file lines are 1 indexed
        for index, line in enumerate(self.origlines[startline - 1:]):
            open_par_nb, has_backslash = eval_continuation(line, open_par_nb)
            if not open_par_nb and not has_backslash:
                return index + startline

        assert False, "bug"

### End of real code


### Stuff to run this as a script

def main(infile, outfile):
    """
    infile: a file descriptor like (must return lines when iterated over)
    outfile: a file descriptor like (must have a write() method)
    """
    neworder = NewOrder(infile)
    neworder.reorder(outfile)

def _parseargs():
    """
    returns parsed sys.argv
    """
    from argparse import ArgumentParser
    from sys import stdin, stdout
    parser = ArgumentParser(
            description="""A tool for reordering
            import statements inside Python code blocks.
            Blocks separated by anything (white line for instance)
            are considered separately.
            """,
            epilog="""Limitations: This script will only handle first level statements.
            This script will not handle several "import module" for the same module in
            the same block.
            """,
            )
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument(
        '--infile',
        default=stdin,
        help='a Python source file, defaults to standard input',
        type=lambda name: open(name, 'r')
        )
    parser.add_argument(
        '--outfile',
        default=stdout,
        help='output, defaults to standard output',
        type=lambda name: open(name, 'w')
        )
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = _parseargs()
    main(ARGS.infile, ARGS.outfile)

