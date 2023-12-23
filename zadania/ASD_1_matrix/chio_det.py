from matrix import Matrix


def chio_determinant(matrix: Matrix) -> float:
    m, n = matrix.size()
    if m != n or len(matrix.size()) != 2:
        raise ValueError("Invalid matrix shape!")

    if m == 1:
        return matrix[0][0]

    col1 = [matrix[i][0] for i in range(m)]
    swap = False
    if matrix[0][0] == 0 and any(col1):
        # Pierwszy element zerowy i jest inny niezerowy element w pierwszej kolumnie
        row_idx = [matrix[i][0] == 0 for i in range(m)].index(False)
        matrix[0], matrix[row_idx] = matrix[row_idx], matrix[0]  # Zamiana wierszy
        swap = True
    elif not any(col1):  # Cała pierwsza kolumna zerowa - macierz osobliwa
        return 0

    new_matrix = Matrix((m - 1, m - 1))
    for i in range(m - 1):
        for j in range(m - 1):
            new_matrix[i][j] = det2x2(Matrix(
                [[matrix[0][0], matrix[0][j + 1]],
                 [matrix[i + 1][0], matrix[i + 1][j + 1]]]))

    return ((-1) / (matrix[0][0]) ** (m - 2)) * chio_determinant(new_matrix) if swap else \
           (1 / (matrix[0][0]) ** (m - 2)) * chio_determinant(new_matrix)


def det2x2(matrix: Matrix) -> float:
    if matrix.size() != (2, 2):
        raise ValueError("Invalid matrix shape!")

    return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]


def main():
    m1 = Matrix([
        [5, 1, 1, 2, 3],
        [4, 2, 1, 7, 3],
        [2, 1, 2, 4, 7],
        [9, 1, 0, 7, 0],
        [1, 4, 7, 2, 2]])

    m2 = Matrix([
        [0, 1, 1, 2, 3],
        [4, 2, 1, 7, 3],
        [2, 1, 2, 4, 7],
        [9, 1, 0, 7, 0],
        [1, 4, 7, 2, 2]])

    print("Wyzancznik macierzy m1:", chio_determinant(m1))
    print("Wyzancznik macierzy m2:", chio_determinant(m2))


if __name__ == '__main__':
    main()
