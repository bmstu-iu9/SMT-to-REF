import ply.yacc as yacc
from Lexer import tokens, find_column

options = {
    'strings-exp': False,
    'produce-models': False
}

funcs = set()


class Error(Exception):
    """Base error class"""
    pass


class WrongOptionError(Error):
    def __init__(self, message):
        self.message = message


class BadArgumentError(Error):
    def __init__(self, message):
        self.message = message


class UndeclaredIdentError(Error):
    def __init__(self, message):
        self.message = message


class GenericError(Error):
    def __init__(self, message):
        self.message = message


def p_program(p):
    """program : logic options decls asserts build
               | logic decls asserts build"""
    p[0] = ('program',) + tuple(p[1:])


def p_logic(p):
    """logic : LPAREN SETLOGIC QF_SLIA RPAREN
             | LPAREN SETLOGIC QF_S RPAREN"""
    p[0] = ('logic',) + tuple(p[1:])


def p_options(p):
    """options : option
               | options option"""
    p[0] = ('options',) + tuple(p[1:])


def p_option(p):
    """option : LPAREN SETOPTION COLON optionname BOOL RPAREN"""
    p[0] = ('option',) + tuple(p[1:])
    options[p[4][1]] = p[5]


def p_optionname(p):
    """optionname : PRODUCEMODELS
                  | STRINGSEXP"""
    p[0] = ('optionname', p[1])


def p_decls(p):
    """decls : decl
             | decls decl"""
    p[0] = ('decls',) + tuple(p[1:])


def p_decl(p):
    """decl : LPAREN DECLAREFUN ID LPAREN RPAREN STRING RPAREN"""
    p[0] = ('decl',) + tuple(p[1:])
    funcs.add(p[3])


def p_asserts(p):
    """asserts : assert
             | asserts assert"""
    p[0] = ('asserts',) + tuple(p[1:])


def p_assert(p):
    """assert : LPAREN ASSERT expr RPAREN"""
    p[0] = ('assert',) + tuple(p[1:])


def p_expr(p):
    """expr : pred
            | LPAREN AND exprs RPAREN
            | LPAREN OR exprs RPAREN
            | LPAREN NOT expr RPAREN"""
    p[0] = ('expr',) + tuple(p[1:])


def p_exprs(p):
    """exprs : expr
             | exprs expr"""
    p[0] = ('exprs',) + tuple(p[1:])


def p_pred(p):
    """pred : LPAREN EQUALS str str RPAREN
            | LPAREN CONTAINS str const RPAREN"""
    if p[2] == 'str.contains' and not options['strings-exp']:
        raise WrongOptionError('Use of \'contains\' with strings-exp set to false!')
    p[0] = ('pred',) + tuple(p[1:])


def p_pred_error(p):
    """pred : LPAREN CONTAINS str error RPAREN"""
    raise BadArgumentError('Second argument of \'contains\' must be a constant!\n')


def p_id(p):
    """str : ID"""
    if p[1] not in funcs:
        raise UndeclaredIdentError('Use of undeclared identifier {}!'.format(p[1]))
    p[0] = ('str',) + tuple(p[1:])


def p_str(p):
    """str : const
           | LPAREN CONCAT strs RPAREN"""
    p[0] = ('str',) + tuple(p[1:])


def p_const(p):
    """const : CONST"""
    p[0] = ('const',) + tuple(p[1:])


def p_replaceall(p):
    """str : LPAREN REPLACEALL str const const RPAREN"""
    if not options['strings-exp']:
        raise WrongOptionError('Use of \'replace_all\' with strings-exp set to false!')
    if not p[4]:
        raise BadArgumentError('Cannot replace an empty string!')
    p[0] = ('str',) + tuple(p[1:])


def p_replaceall_error(p):
    """str : LPAREN REPLACEALL str error const RPAREN
           | LPAREN REPLACEALL str const error RPAREN
           | LPAREN REPLACEALL str error error RPAREN"""
    raise BadArgumentError('Second and third arguments of \'replace_all\' must be constants!\n')


def p_strs(p):
    """strs : str
            | strs str"""
    p[0] = ('strs',) + tuple(p[1:])


def p_build(p):
    """build : LPAREN CHECKSAT RPAREN LPAREN GETMODEL RPAREN"""
    p[0] = ('logic',) + tuple(p[1:])


def p_error(p):
    print('Unexpected token \'{}\' at ({}, {})!'.format(p.value, p.lineno, find_column(p)))


parser = yacc.yacc()


def collapse_asserts(tree):
    tree_as_list = list(tree)
    asserts_index = 4 if len(tree) == 6 else 3
    asserts_node = tree[asserts_index]
    if len(asserts_node) == 3:
        expr = asserts_node[2][3]
        exprs = ('exprs', expr)
        asserts_node = asserts_node[1]
        while len(asserts_node) == 3:
            expr_ = asserts_node[2][3]
            exprs = ('exprs', exprs, expr_)
        expr_ = asserts_node[1][3]
        exprs = ('exprs', exprs, expr_)
        new_node = ('asserts', ('assert', '(', 'assert', ('expr', '(', 'and', exprs)))
        tree_as_list[asserts_index] = new_node
    return tuple(tree_as_list)
