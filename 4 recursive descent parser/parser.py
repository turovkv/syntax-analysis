import sys
import lexer

sys.setrecursionlimit(10 ** 6)


class Parser:
    def __init__(self, string):
        self.lex = lexer.get_lexer(string)
        self.current = next(self.lex)
        self.last_error = None

    def expect(self, token_type):
        if self.current is None:
            self.last_error = f'Error! Expected {token_type}, but EndOfFile found'
            return False
        if self.current.type == token_type:
            self.current = next(self.lex)
            return True
        self.last_error = f'Error! Expected {token_type}' + \
                          f' in line {self.current.lineno}' + \
                          f' in pos {self.current.lexpos - lexer.line_start_pos + 1}'
        return False

    def definition(self):
        if self.current is None:
            self.last_error = None
            return False
        if not self.expect('IDENTIFIER'):
            return False
        if self.expect('END'):
            self.last_error = None
            return True
        if self.expect('DEFINITION') and \
                self.disjunction() and \
                self.expect('END'):
            self.last_error = None
            return True
        return False

    def disjunction(self):
        if not self.conjunction():
            return False
        if self.expect('OR'):
            if not self.disjunction():
                return False
        return True

    def conjunction(self):
        if not self.lowest_expr():
            return False
        if self.expect('AND'):
            if not self.conjunction():
                return False
        return True

    def lowest_expr(self):
        if self.expect('LPAREN'):
            if self.disjunction() and \
                    self.expect('RPAREN'):
                return True
            else:
                return False

        if self.expect('IDENTIFIER'):
            return True
        return False
