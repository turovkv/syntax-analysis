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


def t_error(t):
    error_msg = "SYNTAX ERROR (illegal character)"
    if t:
        error_msg += f" in line {t.lineno} in pos {t.lexpos - line_start_pos + 1} !"
    else:
        error_msg += " at EOF !"
    raise SyntaxError(error_msg)


lexer = lex.lex()