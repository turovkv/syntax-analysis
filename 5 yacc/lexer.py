import ply.lex as lex

reserved = {}

tokens = [
             'IDENTIFIER',
             'DEFINITION',
             'END',
             'AND',
             'OR',
             'LBR',
             'RBR'
         ] + list(reserved.values())


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


t_DEFINITION = r':-'

t_END = r'\.'

t_AND = r','

t_OR = r';'

t_LBR = r'\('

t_RBR = r'\)'

t_ignore = ' \t'

line_start_pos = 0


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    global line_start_pos
    line_start_pos = t.lexpos + len(t.value)


def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()