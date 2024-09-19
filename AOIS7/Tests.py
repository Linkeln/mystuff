import unittest
from main import *

class TestDiagonalMatrix(unittest.TestCase):

    def setUp(self):
        self.matrix_data = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.diagonal_matrix = DiagonalMatrix(self.matrix_data)

    def test_get_diagonal(self):
        self.assertEqual(self.diagonal_matrix.get_diagonal(0, 3), [1, 5, 9])
        self.assertEqual(self.diagonal_matrix.get_diagonal(1, 2), [4, 8])
        self.assertEqual(self.diagonal_matrix.get_diagonal(2, 1), [7])

    def test_set_diagonal(self):
        self.diagonal_matrix.set_diagonal(0, [9, 5, 1])
        self.assertEqual(self.diagonal_matrix.get_diagonal(0, 3), [9, 5, 1])


    def test_get_column(self):
        self.assertEqual(self.diagonal_matrix.get_column(0, 3), [1, 4, 7])
        self.assertEqual(self.diagonal_matrix.get_column(1, 3), [5, 8, 2])

    def test_set_column(self):
        self.diagonal_matrix.set_column(0, [9, 4, 7])
        self.assertEqual(self.diagonal_matrix.get_column(0, 3), [9, 4, 7])

    def test_add_ab(self):
        matrix_data = [
            [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
            [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
            [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
            [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1],
            [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        ]
        dm = DiagonalMatrix(matrix_data)
        result = dm.add_ab('100')
        self.assertIsNotNone(result)

    def test_f0(self):
        result = self.diagonal_matrix.f0(0, 0)
        self.assertEqual(result, [0, 0, 0])

    def test_f5(self):
        result = self.diagonal_matrix.f5(0, 0)
        self.assertEqual(result, [1, 5, 9, 1])

    def test_f10(self):
        result = self.diagonal_matrix.f10(0, 0)
        self.assertEqual(result, [0, 0, 0, 0])

    def test_f15(self):
        result = self.diagonal_matrix.f15(0, 0)
        self.assertEqual(result, [1, 1, 1])

if __name__ == '__main__':
    unittest.main()