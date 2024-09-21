import unittest
from main import *

class TestLogicalFunctions(unittest.TestCase):

    def test_replace_operators(self):
        expr = '!a & b | c -> d ~ e'
        expected = ' not a  and  b  or  c  <=  d  ==  e'
        result = replace_operators(expr)
        self.assertEqual(result, expected)

    def test_evaluate_expression(self):
        expr = 'a & !b'
        vars_values = (True, False)
        result = evaluate_expression(expr, vars_values)
        self.assertTrue(result)

    def test_truth_table(self):
        expr = 'a | b'
        active_vars, results = truth_table(expr)
        expected_results = [
            ((0, 0), False),
            ((0, 1), True),
            ((1, 0), True),
            ((1, 1), True)
        ]
        self.assertEqual(active_vars, 2)
        self.assertEqual(results, expected_results)

    def test_build_sdnf_cnf_forms(self):
        rows = [
            ((0, 0), False),
            ((0, 1), True),
            ((1, 0), True),
            ((1, 1), True)
        ]
        active_vars = 2
        sdnf, cnf = build_sdnf_cnf_forms(rows, active_vars)
        self.assertEqual(sdnf, '!a & b | a & !b | a & b')
        self.assertEqual(cnf, '(!a | !b)')

    def test_merge_terms(self):
        term1 = ['1', '0', '-']
        term2 = ['1', '1', '-']
        result = merge_terms(term1, term2)
        expected = ['1', '-', '-']
        self.assertEqual(result, expected)

    def test_find_implicants(self):
        minterms = [['1', '0', '0'], ['1', '1', '0'], ['0', '1', '0']]
        result = find_implicants(minterms)
        expected = {('1', '-', '0'), ('-', '1', '0')}
        self.assertEqual(result, expected)

    def test_identify_essential_implicants(self):
        implicants = {('1', '-', '0'), ('0', '1', '0')}
        minterms = [['1', '0', '0'], ['1', '1', '0']]
        result = identify_essential_implicants(implicants, minterms)
        expected = {('1', '-', '0')}
        self.assertEqual(result, expected)

    def test_minimize_using_qm(self):
        entries = [
            (('1', '0', '0'), True),
            (('1', '1', '0'), True),
            (('0', '1', '0'), False),
            (('0', '0', '1'), False)
        ]
        active_vars = 3
        is_sdnf = True

        essential_implicants, remaining_minterms = minimize_using_qm(entries, active_vars, is_sdnf)

        expected_essential_implicants = {('1', '1', '0'), ('1', '0', '0')}
        expected_remaining_minterms = []

        self.assertEqual(essential_implicants, expected_essential_implicants)
        self.assertEqual(remaining_minterms, expected_remaining_minterms)


    def test_format_result_sdnf(self):
        implicant = ('1', '-', '0')
        active_vars = 3
        result = format_result(implicant, active_vars, is_sdnf=True)
        expected = '!a & !c'
        self.assertEqual(result, expected)

    def test_format_result_cnf(self):
        implicant = ('0', '1', '-')
        active_vars = 3
        result = format_result(implicant, active_vars, is_sdnf=False)
        expected = '!a | !b'
        self.assertEqual(result, expected)

    def test_generate_implicant_chart(self):
        implicants = {('1', '-', '0'), ('0', '1', '-')}
        minterms = [('1', '0', '0'), ('0', '1', '0'), ('0', '1', '1')]

        result = generate_implicant_chart(implicants, minterms)

        expected = {
            ('1', '0', '0'): [('1', '-', '0')],
            ('0', '1', '0'): [('0', '1', '-')],
            ('0', '1', '1'): [('0', '1', '-')]
        }

        self.assertEqual(result, expected)

    def test_sdnf_case(self):
        entries = [
            ('1000', True),
            ('1010', True),
            ('1100', True),
            ('1110', True),
        ]
        active_vars = ['A', 'B', 'C', 'D']
        essential_implicants_expected = {('1', '-', '-', '0')}
        remaining_minterms_expected = []
        chart_expected = {}

        essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars,
                                                                                             is_sdnf=True)

        self.assertEqual(essential_implicants, essential_implicants_expected)
        self.assertEqual(remaining_minterms, remaining_minterms_expected)
        self.assertEqual(chart, chart_expected)

    def test_sknf_case(self):
        entries = [
            ('0111', False),
            ('1110', False),
            ('1011', False),
            ('1111', False),
        ]
        active_vars = ['A', 'B', 'C', 'D']
        essential_implicants_expected = {('1', '1', '1', '-'), ('1', '-', '1', '1'), ('-', '1', '1', '1')}
        remaining_minterms_expected = []
        chart_expected = {}

        essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars,
                                                                                             is_sdnf=False)

        self.assertEqual(essential_implicants, essential_implicants_expected)
        self.assertEqual(remaining_minterms, remaining_minterms_expected)
        self.assertEqual(chart, chart_expected)

    def test_sdnf_case(self):
        entries = [
            ('00', True),
            ('01', True),
            ('11', True),
            ('10', True),
        ]
        active_vars = 2
        expected_kmap = [
            [1, 1],
            [1, 1]
        ]

        kmap = generate_kmap(entries, active_vars, is_sdnf=True)
        self.assertEqual(kmap, expected_kmap)

    def test_sknf_case(self):
        entries = [
            ('00', False),
            ('01', False),
            ('11', False),
            ('10', False),
        ]
        active_vars = 2
        expected_kmap = [
            [1, 1],
            [1, 1]
        ]

        kmap = generate_kmap(entries, active_vars, is_sdnf=False)
        self.assertEqual(kmap, expected_kmap)

    def test_expression_to_dnf(self):
        expr = "(a & !b) | (b & c)"
        expected_dnf = "(!a & b & c & !d) | (!a & b & c & d) | (a & !b & !c & !d) | (a & !b & !c & d) | (a & !b & c & !d) | (a & !b & c & d) | (a & b & c & !d) | (a & b & c & d)"
        self.assertEqual(expression_to_dnf(expr), expected_dnf)

    def test_expression_to_cnf(self):
        expr = "(a & !b) | (b & c)"
        expected_cnf = "(a | b | c | d) & (a | b | c | !d) & (a | b | !c | d) & (a | b | !c | !d) & (a | !b | c | d) & (a | !b | c | !d) & (!a | !b | c | d) & (!a | !b | c | !d)"
        self.assertEqual(expression_to_cnf(expr), expected_cnf)

    def test_analyze_variable_usage(self):
        expr = "(a & !b) | (b & c) | (a & d) | (a & !d)"
        expected_usage = {'a': 3, 'b': 2, 'c': 1, 'd': 2}
        self.assertEqual(analyze_variable_usage(expr), expected_usage)

    def test_print_normal_forms(self):
        expr = "(a & !b) | (b & c)"

        # Expected results
        expected_dnf = "(!a & b & c & !d) | (!a & b & c & d) | (a & !b & !c & !d) | (a & !b & !c & d) | (a & !b & c & !d) | (a & !b & c & d) | (a & b & c & !d) | (a & b & c & d)"
        expected_cnf = "(a | b | c | d) & (a | b | c | !d) & (a | b | !c | d) & (a | b | !c | !d) & (a | !b | c | d) & (a | !b | c | !d) & (!a | !b | c | d) & (!a | !b | c | !d)"

        # Call the functions directly
        dnf = expression_to_dnf(expr)
        cnf = expression_to_cnf(expr)

        # Assertions
        self.assertEqual(dnf, expected_dnf)
        self.assertEqual(cnf, expected_cnf)

if __name__ == '__main__':
    unittest.main()