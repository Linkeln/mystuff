import unittest
from main import *

class TestLogicalExpressions(unittest.TestCase):
    def test_parse_expression(self):
        self.assertEqual(parse_expression('A & B'), 'A  and  B')
        self.assertEqual(parse_expression('A | B'), 'A  or  B')
        self.assertEqual(parse_expression('!A'), ' not A')
        self.assertEqual(parse_expression('A -> B'), 'A  <=  B')
        self.assertEqual(parse_expression('A ~ B'), 'A  ==  B')

    def test_truth_table(self):
        expr = 'A & B'
        variables = ['A', 'B']
        expected_table = [
            ((False, False), False),
            ((False, True), False),
            ((True, False), False),
            ((True, True), True)
        ]
        self.assertEqual(truth_table(expr, variables), expected_table)

    def test_sdnf_sknf(self):
        table = [
            ((False, False), False),
            ((False, True), False),
            ((True, False), False),
            ((True, True), True)
        ]
        variables = ['A', 'B']
        expected_sdnf = '(A & B)'
        expected_sknf = '(A | B) & (A | !B) & (!A | B)'
        sdnf, sknf = sdnf_sknf(table, variables)
        self.assertEqual(sdnf, expected_sdnf)
        self.assertEqual(sknf, expected_sknf)

    def test_numeric_form(self):
        table = [
            ((False, False), False),
            ((False, True), False),
            ((True, False), False),
            ((True, True), True)
        ]
        variables = ['A', 'B']
        self.assertEqual(numeric_form(table, variables, 'sdnf'), [3])
        self.assertEqual(numeric_form(table, variables, 'sknf'), [0, 1, 2])

    def test_index_form_binary(self):
        self.assertEqual(index_form_binary([3]), '00010000')

    def test_index_form_decimal(self):
        self.assertEqual(index_form_decimal('00001000'), 8)

if __name__ == "__main__":
    unittest.main()