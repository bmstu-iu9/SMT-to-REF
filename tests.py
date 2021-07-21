import Parser
import Lexer
import unittest


class TestSuccesses(unittest.TestCase):
    def setUp(self):
        Parser.funcs.clear()

    def test_0(self):
        with open('tests/test0.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertNotEqual(Parser.parser.parse(data), None)

    def test_1(self):
        with open('tests/test1.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertNotEqual(Parser.parser.parse(data), None)

    def test_2(self):
        with open('tests/test2.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertNotEqual(Parser.parser.parse(data), None)

    def test_3(self):
        with open('tests/test3.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertNotEqual(Parser.parser.parse(data), None)

    def test_4(self):
        with open('tests/test4.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertNotEqual(Parser.parser.parse(data), None)

    def test_5(self):
        with open('tests/test5.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertNotEqual(Parser.parser.parse(data), None)

    def test_6(self):
        with open('tests/test6.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertNotEqual(Parser.parser.parse(data), None)


class TestErrors(unittest.TestCase):
    def setUp(self):
        Parser.funcs.clear()

    def test_bad_func(self):
        with open('tests/test_badfunc.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertRaises(Parser.UndeclaredIdentError, Parser.parser.parse, data)

    def test_bad_replaceall(self):
        with open('tests/test_replaceall.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertRaises(Parser.BadArgumentError, Parser.parser.parse, data)

    def test_bad_contains(self):
        with open('tests/test_contains.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertRaises(Parser.BadArgumentError, Parser.parser.parse, data)

    def test_bad_parentheses(self):
        with open('tests/test_bad_parentheses.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertEqual(Parser.parser.parse(data), None)

    def test_parentheses_inside_const(self):
        with open('tests/test_parentheses_inside_const.smt2', 'r') as input_file:
            data = input_file.read()
        self.assertRaises(Lexer.IllegalCharacterError, Parser.parser.parse, data)


if __name__ == '__main__':
    unittest.main()
