from typing import List, Union, Tuple


class Matrix:
    def __init__(self, matrix: Union[List[List], Tuple], initial_digit: Union[int, float] = 0) -> None:
        if isinstance(matrix, tuple):
            size = matrix
            self.__matrix = [[initial_digit] * size[1] for _ in range(size[0])]

        else:
            self.__matrix = matrix

    def __add__(self, other):
        s_size = self.size()
        o_size = other.size()
        sum_matrix = Matrix((s_size[0], s_size[1]))

        if o_size == s_size:
            for i in range(s_size[0]):
                for j in range(s_size[1]):
                    sum_matrix[i][j] = self[i][j] + other[i][j]
        else:
            raise ValueError("Invalid shapes!")

        return sum_matrix

    def __mul__(self, other):
        row1, col1 = self.size()
        row2, col2 = other.size()
        mul_matrix = Matrix((row1, col2))

        if col1 == row2:
            for i in range(row1):
                for j in range(col2):
                    for k in range(col1):
                        mul_matrix[i][j] += self[i][k] * other[k][j]
        else:
            raise ValueError("Invalid shapes!")

        return mul_matrix

    def __getitem__(self, item):
        return self.__matrix[item]

    def __setitem__(self, key, value):
        self.__matrix[key] = value

    def __str__(self) -> str:
        matrix_str = ''
        for row in self.__matrix:
            for el in row:
                matrix_str += str(el) + ' '
            matrix_str = matrix_str[:-1] + '\n'

        return matrix_str

    def size(self) -> Tuple:
        return len(self.__matrix), len(self[0])


def transpose(matrix: Matrix) -> Matrix:
    t_matrix = Matrix((matrix.size()[1], matrix.size()[0]))
    for i in range(matrix.size()[0]):
        for j in range(matrix.size()[1]):
            t_matrix[j][i] = matrix[i][j]

    return t_matrix


def main():
    m1 = Matrix(
        [[1, 0, 2],
         [-1, 3, 1]]
    )

    m2 = Matrix(
        [[3, 1],
         [2, 1],
         [1, 0]]
    )

    m3 = Matrix(
        [[1, 1, 1],
         [1, 1, 1]]
    )

    print("m1 * m2:\n" + str(m1 * m2))
    print("m1 + m3:\n" + str(m1 + m3))
    print("Transpozycja m1:\n" + str(transpose(m1)))

    print(m1)


if __name__ == '__main__':
    main()
