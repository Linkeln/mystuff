import unittest
from main import *

class TestQuineMcCluskey(unittest.TestCase):

    def test_merge_terms(self):
        self.assertEqual(merge_terms([1, 0, 1], [1, 0, 0]), [1, 0, '-'])
        self.assertEqual(merge_terms([1, 1, 1], [0, 1, 1]), ['-', 1, 1])
        self.assertIsNone(merge_terms([1, 0, 1], [0, 1, 0]))
        self.assertIsNone(merge_terms([1, 1, 1], [1, 1, 1]))

    def test_find_implicants(self):
        minterms = [[1, 0, 0], [1, 0, 1], [1, 1, 0], [0, 1, 1]]
        result = find_implicants(minterms)
        expected = {(1, '-', 0), (1, 0, '-'), (0, 1, 1)}
        self.assertEqual(result, expected)

    def test_quine_mccluskey_with_chart_display(self):
        entries = [([1, 0, 0], True), ([1, 0, 1], True), ([1, 1, 0], True), ([0, 1, 1], True)]
        essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, 3)
        expected_essential_implicants = {(1, '-', 0), (0, 1, 1), (1, 0, '-')}
        expected_remaining_minterms = []
        self.assertEqual(essential_implicants, expected_essential_implicants)
        self.assertEqual(remaining_minterms, expected_remaining_minterms)

    def test_no_matching_implicants(self):
        implicants = {('1', '1', '1')}
        minterms = [[0, 0, 0]]
        expected_chart = {
            (0, 0, 0): []
        }
        chart = generate_implicant_chart(implicants, minterms)
        self.assertEqual(chart, expected_chart)

    def test_display_implicant_chart(self):
        chart = {
            (1, 0, 0): [('1', '0', '-')],
            (1, 0, 1): [('1', '0', '-')]
        }
        self.assertTrue(display_implicant_chart(chart))

    def test_display_minimized_result(self):
        essential_implicants = {('1', '0', '-'), ('-', '1', '1')}
        self.assertTrue(display_minimized_result(essential_implicants, 3, 'ABC', True))

    def test_format_result(self):
        implicant = ('1', '-', '0')
        result = format_result(implicant, 3, 'ABC', True)
        expected_result = '!A & !C'
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()