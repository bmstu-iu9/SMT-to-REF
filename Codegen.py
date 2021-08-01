from re import match


class Converter:
    regex = '[a-zA-Z0-9]'

    def __init__(self, cnf, preds):
        self.cnf = cnf
        self.preds = dict()
        for i in preds:
            self.preds[i[0]] = i[1:]
        self.decls = set()
        self.decls.add('AND {\n'
                       '    e.x1 False e.x2 = False;\n'
                       '    e.Z = True;\n'
                       '}\n')
        self.decls.add('OR {\n'
                       '    e.x1 True e.x2 = True;\n'
                       '    e.Z = False;\n'
                       '}\n')
        self.sent = ''
        self.entry = ''

    @staticmethod
    def screen_const_for_name(const):
        return ''.join([i if match(Converter.regex, i) else '_{}'.format(ord(i)) for i in const[1:-1]])

    @staticmethod
    def screen_id(id_):
        return ''.join([i if match(Converter.regex, i) else '_{}'.format(ord(i)) for i in id_])

    def convert_pred(self, literal):
        if literal[1] == '=':
            self.decls.add('Equal {\n'
                           '    (e.1)(e.1) = True;\n'
                           '    (e.1)(e.2) = False;\n'
                           '}\n')
            return '<Equal ({}) ({})>'.format(self.convert(literal[2]), self.convert(literal[3]))
        if literal[1] == 'str.contains':
            const = self.convert(literal[3])
            name_const = Converter.screen_const_for_name(const)
            self.decls.add('Infix__' + name_const + ' {\n'
                           '    e.1 ' + const + ' e.2 = True;\n'
                           '    e.Z = False;\n'
                           '}\n')
            return '<Infix__{} {}>'.format(name_const, self.convert(literal[2]))

    def convert_not_pred(self, literal):
        if literal[1] == '=':
            self.decls.add('Inequal {\n'
                           '    (e.1)(e.1) = True;\n'
                           '    (e.1)(e.2) = False;\n'
                           '}\n')
            return '<Inequal ({}) ({})>'.format(self.convert(literal[2]), self.convert(literal[3]))
        if literal[1] == 'str.contains':
            const = self.convert(literal[3])
            name_const = Converter.screen_const_for_name(const)
            self.decls.add('No__' + name_const + ' {\n'
                           '    e.1 ' + const + ' e.2 = False;\n'
                           '    e.Z = True;\n'
                           '}\n')
            return '<No__{} {}>'.format(name_const, self.convert(literal[2]))

    def convert(self, literal):
        if literal[0] == 'const':
            return '\'' + literal[1].replace('\\', '\\\\').replace('\'', '\\\'') + '\''
        if literal[0] == 'strs':
            return self.convert(literal[1]) + (' ' + self.convert(literal[2]) if len(literal) == 3 else '')
        if literal[0] == 'str':
            if literal[1] == '(':
                if literal[2] == 'str.++':
                    return self.convert(literal[3])
                if literal[2] == 'str.replace_all':
                    const1 = self.convert(literal[4])
                    const2 = self.convert(literal[5])
                    name_const1 = Converter.screen_const_for_name(const1)
                    name_const2 = Converter.screen_const_for_name(const2)
                    self.decls.add('Repl__' + name_const1 + '__' + name_const2 + ' {\n'
                                   '    e.1 ' + const1 + ' e.2 = e.1 ' + const2 + ' <Repl__' + name_const1 + '__' + name_const2 + ' e.2>;\n'
                                   '    e.Z = e.Z;\n'
                                   '}\n')
                    return '<Repl__' + name_const1 + '__' + name_const2 + ' ' + self.convert(literal[3]) + '>'
            if type(literal[1]) is str:
                return 'e.' + Converter.screen_id(literal[1].replace('\\', '\\\\').replace('\'', '\\\''))
            if type(literal[1]) is tuple:
                return self.convert(literal[1])

    def codegen_disj(self, disj):
        if len(disj) == 2:
            return self.convert_pred(self.preds[disj[1][2]])
        if disj[2] == 'not':
            return self.convert_not_pred(self.preds[disj[3][1][2]])
        if disj[2] == 'or':
            lits = disj[3]
            out = '<OR '
            while len(lits) == 3:
                lit = lits[2]
                out += self.codegen_disj(lit) + ' '
                lits = lits[1]
            out += self.codegen_disj(lits[1]) + '>'
            return out

    def codegen(self):
        decls = self.cnf[3] if len(self.cnf) == 6 else self.cnf[2]
        es = ''
        while len(decls) == 3:
            es += '(e.{}) '.format(Converter.screen_id(decls[2][3]))
            decls = decls[1]
        es += '(e.{})'.format(Converter.screen_id(decls[1][3]))

        asserts = self.cnf[4] if len(self.cnf) == 6 else self.cnf[3]

        self.entry = '$ENTRY Go {\n'
        self.entry += '  ' + es + '\n'
        if len(asserts[1][3]) == 2:
            self.entry += '       = ' + self.codegen_disj(asserts[1][3]) + ';\n'
        elif asserts[1][3][2] == 'and':
            disjs = asserts[1][3][3]
            self.entry += '      = <AND\n'
            while len(disjs) == 3:
                disj = disjs[2]
                self.entry += '          ' + self.codegen_disj(disj) + '\n'
                disjs = disjs[1]
            self.entry += '          ' + self.codegen_disj(disjs[1]) + '\n       >;\n'
        elif asserts[1][3][2] == 'or':
            self.entry += '       = ' + self.codegen_disj(asserts[1][3]) + ';\n'
        self.entry += '}\n'
