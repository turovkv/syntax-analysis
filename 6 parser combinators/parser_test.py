import parser


def test_unit_atom_ok():
    res = lambda x: parser.PrologParsers.atom.parse(x)
    print_res = lambda x: parser.printAST(res(x).value)
    assert print_res('a') == 'Atom (ID (a))'
    assert print_res('a a') == 'Atom (ID (a)) (Atom (ID (a)))'
    assert print_res('a a a') == 'Atom (ID (a)) (Atom (ID (a))) (Atom (ID (a)))'
    assert print_res('a a a a') == 'Atom (ID (a)) (Atom (ID (a))) (Atom (ID (a))) (Atom (ID (a)))'
    assert print_res('a (a a a)') == 'Atom (ID (a)) (Atom (ID (a)) (Atom (ID (a))) (Atom (ID (a))))'
    assert print_res('a (a a a) a') == 'Atom (ID (a)) (Atom (ID (a)) (Atom (ID (a))) (Atom (ID (a)))) (Atom (ID (a)))'
    assert print_res('a (a) (a)') == 'Atom (ID (a)) (Atom (ID (a))) (Atom (ID (a)))'
    assert print_res('a (((a))) (((a)))') == 'Atom (ID (a)) (Atom (ID (a))) (Atom (ID (a)))'
    assert print_res('a ((a (((a)))))') == 'Atom (ID (a)) (Atom (ID (a)) (Atom (ID (a))))'
    assert print_res('a A A') == 'Atom (ID (a)) (Var (A)) (Var (A))'


def test_unit_atom_error():
    res = lambda x: parser.PrologParsers.atom.parse(x)
    print_res = lambda x: parser.printAST(res(x).value)
    assert isinstance(res('(a)'), parser.Failure)
    assert isinstance(res('(a) a'), parser.Failure)
    assert isinstance(res('a ((a) (a))'), parser.Failure)
    assert isinstance(res('A'), parser.Failure)
    assert isinstance(res('A a'), parser.Failure)
    assert isinstance(res('a (A a)'), parser.Failure)
    assert isinstance(res('A a a a'), parser.Failure)
    assert isinstance(res('type'), parser.Failure)
    assert isinstance(res('module'), parser.Failure)


def test_unit_typeexpr_ok():
    res = lambda x: parser.PrologParsers.typeexpr.parse(x)
    print_res = lambda x: parser.printAST(res(x).value)
    assert print_res('a') == 'Type (Atom (ID (a)))'
    assert print_res('a -> a') == 'Arrow (Type (Atom (ID (a)))) (Type (Atom (ID (a))))'
    assert print_res('(((a))) -> a') == 'Arrow (Type (Atom (ID (a)))) (Type (Atom (ID (a))))'
    assert print_res('a -> (((a)))') == 'Arrow (Type (Atom (ID (a)))) (Type (Atom (ID (a))))'
    assert print_res('((((((a))) -> (((a))))))') == 'Arrow (Type (Atom (ID (a)))) (Type (Atom (ID (a))))'
    assert print_res('a a -> a a') == 'Arrow (Type (Atom (ID (a)) (Atom (ID (a))))) (Type (Atom (ID (a)) (Atom (ID (a)))))'
    assert print_res('a a -> A') == 'Arrow (Type (Atom (ID (a)) (Atom (ID (a))))) (Type (Var (A)))'
    assert print_res('(a -> a) -> a') == 'Arrow (Arrow (Type (Atom (ID (a)))) (Type (Atom (ID (a))))) (Type (Atom (ID (a))))'
    assert print_res('(a -> a -> a) -> a') == 'Arrow (Arrow (Type (Atom (ID (a)))) (Arrow (Type (Atom (ID (a)))) (' \
                                              'Type (Atom (ID (a)))))) (Type (Atom (ID (a))))'
    assert print_res('(a -> a) -> (a -> a)') == 'Arrow (Arrow (Type (Atom (ID (a)))) (Type (Atom (ID (a))))) (Arrow (' \
                                                'Type (Atom (ID (a)))) (Type (Atom (ID (a)))))'


def test_unit_typeexpr_error():
    res = lambda x: parser.PrologParsers.typeexpr.parse(x)
    print_res = lambda x: parser.printAST(res(x).value)
    assert isinstance(res('a (->) a'), parser.Failure)
    assert isinstance(res('a ->'), parser.Failure)
    assert isinstance(res('-> a'), parser.Failure)
    assert isinstance(res('a -> -> a'), parser.Failure)
    assert isinstance(res('->'), parser.Failure)
    assert isinstance(res('a -> A a'), parser.Failure)
    assert isinstance(res('a -> a a)'), parser.Failure)


def test_unit_typedef_ok():
    res = lambda x: parser.PrologParsers.typedef.parse(x)
    print_res = lambda x: parser.printAST(res(x).value)
    assert print_res('type a a.') == 'Typedef (ID (a)) (Type (Atom (ID (a))))'
    assert print_res('type a a->a.') == 'Typedef (ID (a)) (Arrow (Type (Atom (ID (a)))) (Type (Atom (ID (a)))))'
    assert print_res('type aA a.') == 'Typedef (ID (aA)) (Type (Atom (ID (a))))'


def test_unit_typedef_error():
    res = lambda x: parser.PrologParsers.typedef.parse(x)
    print_res = lambda x: parser.printAST(res(x).value)
    assert isinstance(res('type '), parser.Failure)
    assert isinstance(res('type .'), parser.Failure)
    assert isinstance(res('type a'), parser.Failure)
    assert isinstance(res('type . a'), parser.Failure)
    assert isinstance(res('type type'), parser.Failure)
    assert isinstance(res('type A a'), parser.Failure)


def test_unit_module_ok():
    res = lambda x: parser.PrologParsers.module.parse(x)
    print_res = lambda x: parser.printAST(res(x).value)
    assert print_res('module a.') == 'Module (ID (a))'
    assert print_res('module aAA.') == 'Module (ID (aAA))'


def test_unit_module_erroe():
    res = lambda x: parser.PrologParsers.module.parse(x)
    print_res = lambda x: parser.printAST(res(x).value)
    assert isinstance(res('module a a.'), parser.Failure)
    assert isinstance(res('modale a a.'), parser.Failure)
    assert isinstance(res('module A.'), parser.Failure)
    assert isinstance(res('module type.'), parser.Failure)
    assert isinstance(res('module a'), parser.Failure)
    assert isinstance(res('module .'), parser.Failure)
    assert isinstance(res('module '), parser.Failure)
    assert isinstance(res('a'), parser.Failure)


def test_unit_relation_ok():
    res = lambda x: parser.PrologParsers.relation.parse(x)
    print_res = lambda x: parser.printAST(res(x).value)
    assert print_res('a :- a.') == 'Relation (Atom (ID (a))) (Atom (ID (a)))'
    assert print_res('a a:- a.') == 'Relation (Atom (ID (a)) (Atom (ID (a)))) (Atom (ID (a)))'
    assert print_res('a :- (((a))).') == 'Relation (Atom (ID (a))) (Atom (ID (a)))'
    assert print_res('a :- a; a.') == 'Relation (Atom (ID (a))) (Disj (Atom (ID (a))) (Atom (ID (a))))'
    assert print_res('a :- a, a.') == 'Relation (Atom (ID (a))) (Conj (Atom (ID (a))) (Atom (ID (a))))'
    assert print_res('a :- (a; a), (a; a).') == 'Relation (Atom (ID (a))) (Conj (Disj (Atom (ID (a))) (Atom (ID (' \
                                                'a)))) (Disj (Atom (ID (a))) (Atom (ID (a)))))'
    assert print_res('a :- a a.') == 'Relation (Atom (ID (a))) (Atom (ID (a)) (Atom (ID (a))))'


def test_unit_relation_erroe():
    res = lambda x: parser.PrologParsers.relation.parse(x)
    print_res = lambda x: parser.printAST(res(x).value)
    assert isinstance(res('a : -'), parser.Failure)
    assert isinstance(res('a :- a'), parser.Failure)
    assert isinstance(res('A :- a.'), parser.Failure)
    assert isinstance(res('a :- A.'), parser.Failure)
    assert isinstance(res('a :- a, .'), parser.Failure)
    assert isinstance(res('a :- a; .'), parser.Failure)
    assert isinstance(res('a :- a; A A.'), parser.Failure)