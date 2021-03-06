import ply.lex as lex


def find_column(token):
    line_start = lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


class Error(Exception):
    """Base error class"""
    pass


class IllegalCharacterError(Error):
    def __init__(self, message):
        self.message = message


reserved = {
    'String': 'STRING',
    'assert': 'ASSERT',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'QF_SLIA': 'QF_SLIA',
    'QF_S': 'QF_S'
}

tokens = [
    'ID',
    'LPAREN',
    'RPAREN',
    'COLON',
    'CONST',
    'SETLOGIC',
    'SETOPTION',
    'PRODUCEMODELS',
    'STRINGSEXP',
    'DECLAREFUN',
    'CONCAT',
    'REPLACEALL',
    'CONTAINS',
    'EQUALS',
    'CHECKSAT',
    'GETMODEL',
    'BOOL'
] + list(reserved.values())


def t_SETLOGIC(t):
    r'set\-logic'
    return t


def t_BOOL(t):
    r'true | false'
    t.value = t.value == 'true'
    return t


def t_SETOPTION(t):
    r'set\-option'
    return t


def t_CONCAT(t):
    r'str\.\+\+'
    return t


def t_REPLACEALL(t):
    r'str\.replace_all'
    return t


def t_CONTAINS(t):
    r'str\.contains'
    return t


def t_EQUALS(t):
    r'\='
    return t


def t_PRODUCEMODELS(t):
    r'produce\-models'
    return t


def t_STRINGSEXP(t):
    r'strings\-exp'
    return t


def t_DECLAREFUN(t):
    r'declare\-fun'
    return t


def t_CHECKSAT(t):
    r'check\-sat'
    return t


def t_GETMODEL(t):
    r'get\-model'
    return t


def t_ID(t):
    r'[a-zA-Z\\~!@\\$%\\^\\&\\*_\\-\\+=<>\\.\\?/][a-zA-Z0-9\\~!@\\$%\\^\\&\\*_\\-\\+=<>\\.\\?/]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_CONST(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise IllegalCharacterError('Illegal character \'{}\' at ({}, {})'.format(t.value[0], lexer.lineno, find_column(t)))


t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'

t_ignore = ' \t'

lexer = lex.lex()

if __name__ == '__main__':
    data = '''
    (set-logic QF_SLIA)
    (set-option :strings-exp true)
    (set-option :produce-models true)

    (declare-fun xvvvvvv112yy () String)

    (assert (str.contains xvvvvvv112yy "ABAAAC"))

    (check-sat)
    (get-model)'''

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)
