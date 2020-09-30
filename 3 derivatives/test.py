import time

from main import *


def test_empty():
    assert not nullable(Empty())


def test_epsilon():
    assert nullable(Epsilon())


def test_char():
    assert not nullable(Char('a'))


def test_alt():
    assert nullable(alt(Epsilon(), Empty()))
    assert nullable(alt(Epsilon(), Epsilon()))
    assert nullable(alt(Epsilon(), Char('a')))
    assert not nullable(alt(Empty(), Char('a')))
    assert not nullable(alt(Empty(), Empty()))
    assert not nullable(alt(Char('a'), Char('b')))


def test_seq():
    assert nullable(alt(Epsilon(), Empty()))
    assert not nullable(seq(Epsilon(), Empty()))
    assert not nullable(seq(Epsilon(), Char('a')))
    assert not nullable(seq(Empty(), Char('a')))
    assert not nullable(seq(Empty(), Empty()))
    assert not nullable(seq(Char('a'), Char('b')))


def test_star():
    assert nullable(star(Char('b')))
    assert nullable(star(Epsilon()))
    assert not nullable(star(Empty()))


def test_plus():
    assert nullable(star(Char('b')))
    assert nullable(star(Epsilon()))
    assert not nullable(star(Empty()))


def test_integration_1():
    exp = seq(seq(star(Char('a')), star(Char('b'))), star(Char('c')))  # (a)*(b)*(c)*
    string = 'a' * 2 * 10 ** 5 + 'bc'
    assert check(string, exp)


def test_integration_2():
    exp = seq(alt(Char('a'), star(Char('a'))), alt(Char('a'), star(Char('a'))))  # (a | a*)(a | a*)
    string = 'a' * 10 ** 6
    assert check(string, exp)


def test_integration_3():
    exp = star(Char('a'))  # a*
    string = 'a' * 10 ** 6
    assert check(string, exp)


def test_integration_4():
    exp = seq(seq(alt(Char('a'), star(Char('a'))), Char('a')), alt(Char('a'), star(Char('a'))))  # (a | a*) a (a | a*)
    string = 'a' * 2 * 10 ** 5
    assert check(string, exp)


def test_integration_5():
    exp = plus(Char('a'))  # a+
    string = 'a' * 2 * 10 ** 5
    assert check(string, exp)


def test_integration_5_1():
    exp = plus(Char('a'))  # a+
    string = 'a' * 10 ** 5 + 'b'
    assert not check(string, exp)


def test_integration_6():
    exp = seq(seq(star(Char('a')), star(Char('a'))), star(Char('a')))   # a*a*a*
    string = 'a' * 10 ** 5
    assert check(string, exp)


def test_integration_7():
    exp = plus(seq(alt(Char('a'), Char('b')), alt(Char('c'), Char('d'))))   # ((a|b)(c|d))+
    string = 'ad' * 10 ** 2
    assert check(string, exp)


def test_integration_7_1():
    exp = plus(seq(alt(Char('a'), Char('b')), alt(Char('c'), Char('d'))))   # ((a|b)(c|d))+
    string = 'ab' * 10 ** 2 + 'ab'
    assert not check(string, exp)
