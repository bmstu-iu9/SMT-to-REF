import ply.yacc as yacc
from Lexer import tokens

options = {
    'strings-exp': False,
    'produce-models': False
}

funcs = set()


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
        print("Use of \'contains\' with strings-exp set to false!")
        exit(3)
    p[0] = ('pred',) + tuple(p[1:])


def p_id(p):
    """str : ID"""
    if p[1] not in funcs:
        print("Use of undeclared identifier {}!", p[1])
        exit(3)
    p[0] = ('str',) + tuple(p[1:])


def p_str(p):
    """str : CONST
           | LPAREN CONCAT strs RPAREN"""
    p[0] = ('str',) + tuple(p[1:])


def p_replaceall(p):
    """str : LPAREN REPLACEALL str CONST CONST RPAREN"""
    if not p[4]:
        print("Cannot replace an empty string!")
        exit(3)
    if not options['strings-exp']:
        print("Use of \'replace_all\' with strings-exp set to false!")
        exit(3)
    p[0] = ('str',) + tuple(p[1:])


def p_strs(p):
    """strs : str
            | strs str"""
    p[0] = ('strs',) + tuple(p[1:])


def p_build(p):
    """build : LPAREN CHECKSAT RPAREN LPAREN GETMODEL RPAREN"""
    p[0] = ('logic',) + tuple(p[1:])


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()

if __name__ == '__main__':
    with open('input', "r") as input_file:
        data = input_file.read()
    result = parser.parse(data)
    print(result)
