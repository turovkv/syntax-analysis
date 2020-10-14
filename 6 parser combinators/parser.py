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
    keywords = {'module', 'type'}
    not_keyword_comb = lambda parser, kw=keywords: pred(parser, lambda x: x not in kw, 'not a keyword')
    identifier = not_keyword_comb(reg(r'[a-z_][a-zA-Z_0-9]*')) > (lambda x: ['ID'] + [x])
    variable = not_keyword_comb(reg(r'[A-Z][a-zA-Z_0-9]*')) > (lambda x: ['Var'] + [x])

    module = 'module' >> identifier << '.' > (lambda x: ['Module'] + [x])

    type = 'type' >> identifier & typeexpr << '.' > (lambda x: ['Typedef'] + [x[0]] + [x[1]])

    typeexpr = rep1sep(inner_type, '->') > (lambda x: x[0] if len(x) == 1 and x[0][0] == 'Type' else ['Type'] + x)
    inner_type = atom | variable | '(' >> inner_type << ')' | '(' >> typeexpr << ')'

    relation = atom & opt(':-' >> disjunction) << '.' > (lambda x: ['Relation'] + [x[0]] + x[1])

    disjunction = rep1sep(conjunction, ';') > (lambda x: ['Disj'] + x)
    conjunction = rep1sep(lowexpr, ',') > (lambda x: ['Conj'] + x)
    lowexpr = atom | '(' >> disjunction << ')' > (lambda x: ['Lowexpr'] + [x])

    atom = identifier & rep(simple_atom | inner_atom) > (lambda x: ['Atom'] + [x[0]] + x[1])
    inner_atom = '(' >> atom << ')' | '(' >> inner_atom << ')'
    simple_atom = identifier | variable > (lambda x: ['Atom'] + [x]) # false

    program = module & rep(type) & rep(relation) > (lambda x: printAST(['Program'] + [x[0]] + x[1] + x[2]))


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file_in, \
            open(sys.argv[1] + '.out', 'w') as file_out:
        res = PrologParsers.program.parse(file_in.read())
        if isinstance(res, Success):
            file_out.write(f'OK !\n{res.value}')
        else:
            file_out.write(f'ERROR !\n{res.message}')
