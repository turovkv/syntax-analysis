import sys

sys.setrecursionlimit(10 ** 6)


class Empty:
    pass


class Epsilon:
    pass


class Char:
    def __init__(self, char):
        self.arg = char


class Alt:
    def __init__(self, left, right):
        self.arg_left = left
        self.arg_right = right


class Seq:
    def __init__(self, left, right):
        self.arg_left = left
        self.arg_right = right


class Star:
    def __init__(self, exp):
        self.arg = exp


def alt(left, right):
    if isinstance(right, Empty):
        left, right = right, left
    if isinstance(left, Empty):
        return right

    if isinstance(right, Epsilon):
        left, right = right, left
    if isinstance(left, Epsilon):
        if nullable(right):
            return right
        else:
            return Alt(left, right)

    if isinstance(right, Star):
        left, right = right, left
    if isinstance(left, Star):
        if equal(left.arg, right):
            return left

    if isinstance(right, Alt):
        left, right = right, left
    if isinstance(right, Alt):
        return alt(alt(left, right.arg_left), right.arg_right)

    def find_in_alts(exp, needle):
        if equal(exp, needle):
            return True
        if isinstance(exp, Alt):
            return find_in_alts(exp.arg_left, needle) or \
                   find_in_alts(exp.arg_right, needle)
        return False

    if find_in_alts(left, right):
        return left

    return Alt(left, right)


def seq(left, right):
    if isinstance(right, Empty):
        left, right = right, left
    if isinstance(left, Empty):
        return Empty()

    if isinstance(right, Epsilon):
        left, right = right, left
    if isinstance(left, Epsilon):
        return right

    if isinstance(right, Seq):
        left, right = right, left
    if isinstance(right, Seq):
        return seq(seq(left, right.arg_left), right.arg_right)

    def find_in_seqs(exp, needle):
        if equal(exp, needle):
            return True
        if isinstance(exp, Seq):
            return find_in_seqs(exp.arg_right, needle)
        return False

    if isinstance(right, Star) and find_in_seqs(left, right):
        return left

    return Seq(left, right)


def star(arg):
    if isinstance(arg, Empty):
        return Empty()
    if isinstance(arg, Epsilon):
        return Epsilon()

    if isinstance(arg, Star):
        return arg

    return Star(arg)


def plus(arg):
    return seq(arg, star(arg))


def equal(a, b):
    if type(a) != type(b):
        return False
    if isinstance(a, Empty):
        return True
    if isinstance(a, Epsilon):
        return True
    if isinstance(a, Char):
        return a.arg == b.arg
    if isinstance(a, Alt) or isinstance(a, Seq):
        return equal(a.arg_left, b.arg_left) and equal(a.arg_right, b.arg_right)
    if isinstance(a, Star):
        return equal(a.arg, b.arg)


def nullable(exp):
    if isinstance(exp, Empty):
        return False
    if isinstance(exp, Epsilon):
        return True
    if isinstance(exp, Char):
        return False
    if isinstance(exp, Alt):
        return nullable(exp.arg_left) or nullable(exp.arg_right)
    if isinstance(exp, Seq):
        return nullable(exp.arg_left) and nullable(exp.arg_right)
    if isinstance(exp, Star):
        return True


def dfs(exp):
    if isinstance(exp, Empty):
        print('Emp', end='')
    if isinstance(exp, Epsilon):
        print('Eps', end='')
    if isinstance(exp, Char):
        print(exp.arg, end='')
    if isinstance(exp, Alt):
        print('(', end='')
        dfs(exp.arg_left)
        print('|', end='')
        dfs(exp.arg_right)
        print(')', end='')
    if isinstance(exp, Seq):
        print('(', end='')
        dfs(exp.arg_left)
        dfs(exp.arg_right)
        print(')', end='')
    if isinstance(exp, Star):
        dfs(exp.arg)
        print('*', end='')


def derivative(char, exp):
    if isinstance(exp, Empty):
        return Empty()
    if isinstance(exp, Epsilon):
        return Empty()

    if isinstance(exp, Char):
        if char == exp.arg:
            return Epsilon()
        else:
            return Empty()

    if isinstance(exp, Alt):
        return alt(derivative(char, exp.arg_left), derivative(char, exp.arg_right))

    if isinstance(exp, Seq):
        if nullable(exp.arg_left):
            return alt(seq(derivative(char, exp.arg_left), exp.arg_right),
                       derivative(char, exp.arg_right))
        else:
            return seq(derivative(char, exp.arg_left), exp.arg_right)

    if isinstance(exp, Star):
        return seq(derivative(char, exp.arg), exp)


def check(string, exp):
    cur_exp = exp
    for char in string:
        cur_exp = derivative(char, cur_exp)
    return nullable(cur_exp)


my_exp = Seq(Alt(Char('a'), Char('b')), Star(Char('c')))
my_exp2 = Seq(Alt(Char('a'), Char('b')), Star(Char('c')))

if __name__ == '__main__':
    print(check(input(), my_exp))
    print(my_exp == my_exp2)
