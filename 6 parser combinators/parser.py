import argparse
from typing import List

from parsita import *
import sys


def printAST(node):
    if not isinstance(node, list):
        return str(node)
    if node[0] == 'Program':
        ans = f'{node[0]} (\n' + '\n'.join(map(printAST, node[1:])) + '\n)'
    else:
        ans = f'{node[0]} (' + ') ('.join(map(printAST, node[1:])) + ')'
    return ans


class PrologParsers(TextParsers, whitespace=r'[ \t\n\r]*'):
    program = opt(module) & rep(typedef) & rep(relation) > (lambda x: ['Program'] + x[0] + x[1] + x[2])

    module = 'module' >> identifier << '.' > (lambda x: ['Module'] + [x])

    typedef = 'type' >> identifier & opt(typeexpr) << '.' > (lambda x: ['Typedef'] + [x[0]] + x[1])
    typeexpr = ((type_arg << '->') & typeexpr > (lambda x: ['Arrow'] + x)) | type_arg
    type_arg = '(' >> typeexpr << ')' | type_simple
    type_simple = atom | variable > (lambda x: ['Type'] + [x])

    relation = atom & opt(':-' >> body) << '.' > (lambda x: ['Relation'] + [x[0]] + x[1])

    body = disjunction
    disjunction = (conjunction << ';' & disjunction > (lambda x: ['Disj'] + x)) | conjunction
    conjunction = (lowexpr << ',' & conjunction > (lambda x: ['Conj'] + x)) | lowexpr
    lowexpr = atom | '(' >> disjunction << ')'

    atom = identifier & rep(simple_atom | inner_atom | variable) > (lambda x: ['Atom'] + [x[0]] + x[1])
    inner_atom = '(' >> inner_atom << ')' | '(' >> atom << ')'
    simple_atom = identifier > (lambda x: ['Atom'] + [x])

    keywords = {'module', 'type'}
    not_keyword_comb = lambda parser, kw=keywords: pred(parser, lambda x: x not in kw, 'not a keyword')
    identifier = not_keyword_comb(reg(r'[a-z_][a-zA-Z_0-9]*')) > (lambda x: ['ID'] + [x])
    variable = not_keyword_comb(reg(r'[A-Z][a-zA-Z_0-9]*')) > (lambda x: ['Var'] + [x])


def main(args: List[str]):
    if len(args) == 1:
        option = None
        filename = args[0]
    elif len(args) == 2:
        option = args[0]
        filename = args[1]
    else:
        print('Invalid args')
        return

    with open(filename, 'r') as file_in, \
            open(filename + '.out', 'w') as file_out:

        if option is None or option == '--prog':
            res = PrologParsers.program.parse(file_in.read())
        elif option == '--atom':
            res = PrologParsers.atom.parse(file_in.read())
        elif option == '--typeexpr':
            res = PrologParsers.typeexpr.parse(file_in.read())
        elif option == '--type':
            res = PrologParsers.typedef.parse(file_in.read())
        elif option == '--module':
            res = PrologParsers.module.parse(file_in.read())
        elif option == '--relation':
            res = PrologParsers.relation.parse(file_in.read())

        if isinstance(res, Success):
            file_out.write(printAST(res.value))
        else:
            file_out.write(f'ERROR !\n{res.message}')


if __name__ == '__main__':
    main(sys.argv[1:])
