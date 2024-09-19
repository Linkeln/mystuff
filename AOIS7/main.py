import random


class DiagonalMatrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0


    def get_diagonal(self, index, length):
        """Получает диагональ по индексу с заданной длиной."""
        diagonal = []
        start_row, start_col = self._get_starting_position(index)

        while len(diagonal) < length:
            if start_row < self.rows and start_col < self.cols:
                diagonal.append(self.matrix[start_row][start_col])
            else:
                diagonal.append(0)  # Заполнение нулями, если вышли за границы
            start_row += 1
            start_col += 1

            if start_row >= self.rows or start_col >= self.cols:
                start_row, start_col = 0, index

        return diagonal


    def set_diagonal(self, index, values):
        """Устанавливает значения диагонали по индексу."""
        start_row, start_col = self._get_starting_position(index)
        i = 0
        while i < len(values):
            if start_row < self.rows and start_col < self.cols:
                self.matrix[start_row][start_col] = values[i]
            start_row += 1
            start_col += 1
            i += 1

            if start_row >= self.rows or start_col >= self.cols:
                start_row, start_col = 0, index


    def _get_starting_position(self, index):
        """Вычисляет начальную позицию для диагонали."""
        if index < self.rows:
            return index, 0
        else:
            return 0, index - self.rows + 1


    def get_column(self, index, length):
        """Получает столбец по индексу с заданной длиной."""
        column = []
        row = index
        while len(column) < length:
            if row < self.rows and index < self.cols:
                column.append(self.matrix[row][index])
            else:
                column.append(0)  # Заполнение нулями, если вышли за границы
            row += 1

            if row >= self.rows:
                row = 0

        return column

    def set_column(self, index, values):
        """Записывает столбец по индексу с заданными значениями."""
        row = index
        for value in values:
            if row < self.rows and index < self.cols:
                self.matrix[row][index] = value
            row += 1

            if row >= self.rows:
                break

    def add_ab(self, V):
        """Adds fields A and B in words where V matches a given value."""
        for index in range(self.rows + self.cols - 1):
            diagonal = self.get_diagonal(index, max(self.rows, self.cols))
            word = ''.join(map(str, diagonal))  # Convert diagonal to string

            if word.startswith(V):

                # Split the word into sections
                V_section = word[:3]
                A_section = word[3:7]
                B_section = word[7:11]
                S_section = word[11:16]

                # Calculate the new S_section
                total_ab = int(A_section, 2) + int(B_section, 2)
                new_S_section = format(total_ab, '05b')

                # Create the new word
                new_word = V_section + A_section + B_section + new_S_section
                new_values = list(map(int, new_word))  # Convert string back to list of integers

                # Update the diagonal
                self.set_diagonal(index, new_values)
                return new_word  # Return the modified word
        return None

    def f0(self, index_1, index_2):
        result = []

        for idk in range(max(self.rows, self.cols)):
            result.append(0)
        return result

    def f5(self, index_1, index_2):
        result = self.get_diagonal(index_2, 4)

        return result

    def f10(self, index_1, index_2):
        result = self.get_diagonal(index_2, 4)

        return [1 if x == 0 else 0 for x in result]

    def f15(self, index_1, index_2):
        result = []

        for idk in range(max(self.rows, self.cols)):
            result.append(1)
        return result

