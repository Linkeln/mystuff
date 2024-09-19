import unittest
from main import *

class TestBinaryFunctions(unittest.TestCase):

    def test_swap_zeros_ones(self):
        self.assertEqual(swap_zeros_ones('101010'), '010101')
        self.assertEqual(swap_zeros_ones('111000'), '000111')
        self.assertEqual(swap_zeros_ones('abc'), 'abc')
        self.assertEqual(swap_zeros_ones(''), '')

    def test_straight_to_decimal(self):
        self.assertEqual(straight_to_decimal('101'), 5)
        self.assertEqual(straight_to_decimal('0'), 0)
        self.assertEqual(straight_to_decimal('1111'), 15)

    def test_decimal_to_binary(self):
        self.assertEqual(decimal_to_binary(5), '00000101')
        self.assertEqual(decimal_to_binary(0), '00000000')
        self.assertEqual(decimal_to_binary(15), '00001111')

    def test_decimal_to_binary_reversed(self):
        self.assertEqual(decimal_to_binary_reversed(5), '00000101')
        self.assertEqual(decimal_to_binary_reversed(-5), '11111010')
        self.assertEqual(decimal_to_binary_reversed(0), '00000000')

    def test_reversed_to_additional(self):
        self.assertEqual(reversed_to_additional('11111011'), '11111100')
        self.assertEqual(reversed_to_additional('00000101'), '00000101')

    def test_summ(self):
        self.assertEqual(summ(5, 3), '00001000')
        self.assertEqual(summ(10, -10), '00000000')

    def test_summ_bin(self):
        self.assertEqual(summ_bin('00000101', '00000011'), '00001000')
        self.assertEqual(summ_bin('00001010', '11110110'), '00000000')

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), '00000010')
        self.assertEqual(subtract(10, 10), '00000000')

    def test_mult(self):
        self.assertEqual(mult(2, 3), '00000100')
        self.assertEqual(mult(4, 5), '00001000')

    def test_binary_division(self):
        quotient, remainder = binary_division('00010000', '00000111')
        self.assertEqual(quotient, 0)
        self.assertEqual(remainder, 0)

    def test_ieee754_addition(self):
        self.assertAlmostEqual(ieee754_addition(1.5, 2.5), 4.0)
        self.assertAlmostEqual(ieee754_addition(-1.5, 2.5), 1.0)

if __name__ == '__main__':
    unittest.main()