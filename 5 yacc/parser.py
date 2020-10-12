import ply.yacc as yacc
import sys
from lexer import tokens


def p_program(p):
    """program : definition
               | definition program"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = f'{p[1]} \n{p[2]}'


def p_definition(p):
    """definition : atom END
                  | atom DEFINITION disjunction END"""
    if len(p) == 3:
        p[0] = f'Def ({p[1]})'
    elif len(p) == 5:
        p[0] = f'Def ({p[1]}) by ({p[3]})'


def p_disjunction(p):
    """disjunction : conjunction
                   | conjunction OR disjunction"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'Disj ({p[1]}) ({p[3]})'


def p_conjunction(p):
    """conjunction : lowexpr
                   | lowexpr AND conjunction"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'Conj ({p[1]}) ({p[3]})'


def p_lowexpr(p):
    """lowexpr : atom
               | LBR disjunction RBR"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'({p[2]})'


def p_atom(p):
    """atom : IDENTIFIER
            | IDENTIFIER atom
            | IDENTIFIER atom2
            | IDENTIFIER atom2 atom"""
    if len(p) == 2:
        p[0] = f'Atom({p[1]})'
    elif len(p) == 3:
        p[0] = f'Atom({p[1]} {p[2]})'
    elif len(p) == 4:
        p[0] = f'Atom({p[1]} {p[2]} {p[3]})'


def p_atom2(p):
    """atom2 : atom3
             | atom3 atom2"""
    if len(p) == 2:
        p[0] = f'{p[1]}'
    elif len(p) == 3:
        p[0] = f'{p[1]} {p[2]}'


def p_atom3(p):
    """atom3 : LBR atom RBR
             | LBR atom3 RBR"""
    if len(p) == 4:
        p[0] = f'{p[2]}'


def p_error(p):
    error_msg = "SYNTAX ERROR"
    if p:
        error_msg += f" in line {p.lineno} in pos {p.lexpos} !"
    else:
        error_msg += " at EOF !"
    raise SyntaxError(error_msg)


parser = yacc.yacc()

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file_in, \
            open(sys.argv[1] + '.out', 'w') as file_out:
        try:
            result = parser.parse(file_in.read())
            file_out.write(f'OK !\n{result}')
        except SyntaxError as e:
            file_out.write(str(e))

