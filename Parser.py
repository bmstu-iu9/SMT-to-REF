import ply.yacc as yacc
from Lexer import tokens, find_column
import Translate
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
            | LPAREN CONTAINS str CONST RPAREN"""
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
    """str : CONST
           | LPAREN CONCAT strs RPAREN"""
    p[0] = ('str',) + tuple(p[1:])


def p_replaceall(p):
    """str : LPAREN REPLACEALL str CONST CONST RPAREN"""
    if not options['strings-exp']:
        raise WrongOptionError('Use of \'replace_all\' with strings-exp set to false!')
    if not p[4]:
        raise BadArgumentError('Cannot replace an empty string!')
    p[0] = ('str',) + tuple(p[1:])


def p_replaceall_error(p):
    """str : LPAREN REPLACEALL str error CONST RPAREN
           | LPAREN REPLACEALL str CONST error RPAREN
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


if __name__ == '__main__':
    with open('tests/test_parentheses_inside_const.smt2', 'r') as input_file:
        data = input_file.read()

    result = parser.parse(data)
    if not result:
        raise GenericError('Parsing failed!')

    result,preds= Translate.translateToCNF(list(result))
    print(result)
    print(preds)
