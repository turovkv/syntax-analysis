from parsita import *
import sys

# def printAST(node):
#     if len(node) == 1:
#         ans = 'ERROR'
#
#     if node[0] == 'Program':
#         ans = '\n'.join(map(printAST, node[1:]))
#     if node[0] == 'Relation':
#         ans = f'relHead ({printAST(node[1])})'
#         if len(node) > 2:
#             ans += ' relBody (' + ' '.join(map(printAST, node[2:])) + ')'
#     if node[0] == 'Disj':
#         if len(node) == 2:
#             ans = printAST(node[1])
#         else:
#             ans = 'Disj (' + ')('.join(map(printAST, node[1:])) + ')'
#     if node[0] == 'Conj':
#         if len(node) == 2:
#             ans = printAST(node[1])
#         else:
#             ans = 'Conj (' + ')('.join(map(printAST, node[1:])) + ')'
#     if node[0] == 'Lowexpr':
#         ans = printAST(node[1]) #???
#     if node[0] == 'Atom':
#         ans = 'Atom (' + ' '.join(map(printAST, node[1:])) + ')'
#     if node[0] == 'ID':
#         ans = f'ID {node[1]}'
#     return ans


# def printAST(node, ident = 0):
#     if not isinstance(node, list):
#         return ' ' * ident + str(node)
#     ans = ''
#     ans += ' ' * ident + f'[{node[0]}\n'
#     ans += '\n'.join(map(lambda x: printAST(x, ident + 4), node[1:])) + '\n'
#     ans += ' ' * ident + ']'
#     return ans


def printAST(node):
    if not isinstance(node, list):
        return str(node)
    if node[0] == 'Program':
        ans = f'{node[0]} (\n' + '\n'.join(map(printAST, node[1:])) + '\n)'
    else:
        ans = f'{node[0]} (' + ')('.join(map(printAST, node[1:])) + ')'
    return ans


class PrologParsers(TextParsers, whitespace=r'[ \t\n\r]*'):
    id = reg(r'[a-zA-Z_][a-zA-Z_0-9]*') > (lambda x: ['ID'] + [x])
    program = rep(relation) > (lambda x: printAST(['Program'] + x))
    relation = atom & opt(':-' >> disjunction) << '.' > (lambda x: ['Relation'] + [x[0]] + x[1])
    disjunction = rep1sep(conjunction, ';') > (lambda x: ['Disj'] + x)
    conjunction = rep1sep(lowexpr, ',') > (lambda x: ['Conj'] + x)
    lowexpr = atom | '(' >> disjunction << ')' > (lambda x: ['Lowexpr'] + [x])
    atom = id & rep(simple_atom | inner_atom) > (lambda x: ['Atom'] + [x[0]] + x[1])
    inner_atom = '(' >> atom << ')' | '(' >> inner_atom << ')'
    simple_atom = id > (lambda x: ['Atom'] + [x])


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file_in, \
            open(sys.argv[1] + '.out', 'w') as file_out:
        res = PrologParsers.program.parse(file_in.read())
        if isinstance(res, Success):
            file_out.write(f'OK !\n{res.value}')
        else:
            file_out.write(f'ERROR !\n{res.message}')

