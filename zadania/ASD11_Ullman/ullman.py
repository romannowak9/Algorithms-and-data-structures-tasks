from copy import deepcopy
from typing import List
from adjacency_matrix import AdjMatrixGraph
from graph import Vertex
import numpy as np


def m0_matrix(p_matrix: np.ndarray, g_matrix: np.ndarray) -> np.ndarray:
    M0 = np.ones((p_matrix.shape[0], g_matrix.shape[0]))
    p_matrix0 = deepcopy(p_matrix)
    g_matrix0 = deepcopy(g_matrix)

    for i, p_row in enumerate(p_matrix0):
        p_deg = sum([(1 if edge_val != 0 else 0) for edge_val in p_row])
        for j, g_row in enumerate(g_matrix0):
            g_deg = sum([(1 if edge_val != 0 else 0) for edge_val in g_row])
            if g_deg < p_deg:
                M0[i][j] = 0

    return M0


def prune(m_matrix_copy: np.ndarray, p_matrix: np.ndarray, g_matrix: np.ndarray) -> bool:
    for i in range(m_matrix_copy.shape[0]):
        for j in range(m_matrix_copy.shape[1]):
            if m_matrix_copy[i, j] == 1:
                p_neighbours = []
                for x in range(p_matrix.shape[0]):
                    if p_matrix[i, x] == 1:
                        p_neighbours.append(x)

                g_neighbours = []
                for y in range(g_matrix.shape[0]):
                    if g_matrix[j, y] == 1:
                        g_neighbours.append(y)

                for x in p_neighbours:
                    is_equivalent = False
                    for y in g_neighbours:
                        if m_matrix_copy[x, y] == 1:
                            is_equivalent = True
                            break

                    if is_equivalent:
                        break
                    else:
                        m_matrix_copy[i, j] = 0
                        return True

    return False


# def prune(m_matrix_copy: np.ndarray, p_matrix: np.ndarray, g_matrix: np.ndarray) -> bool:
#     for i in range(m_matrix_copy.shape[0]):
#         for j in range(m_matrix_copy.shape[1]):
#             if m_matrix_copy[i, j] == 1:
#                 is_equivalent = False
#                 for x in range(p_matrix.shape[0]):
#                     for y in range(g_matrix.shape[0]):
#                         if m_matrix_copy[x, y] == 1:
#                             is_equivalent = True
#                             break
#
#                 if not is_equivalent:
#                     m_matrix_copy[i, j] = 0
#                     return True
#
#     return False

def m_matrix_variations1(M: np.ndarray, P: np.ndarray, G: np.ndarray, M0: np.ndarray, current_row: int = 0,
                         is_col_used: np.ndarray = None, valid_variations: List = None, no_recursion: int = 0):
    if valid_variations is None:
        valid_variations = []

    if is_col_used is None:
        is_col_used = np.array([False for _ in range(M.shape[1])])

    if current_row == M.shape[0]:
        if np.array_equal(P, M @ (M @ G).T):
            valid_variations.append(M)

        return no_recursion

    M_copy = deepcopy(M)
    for c in range(M_copy.shape[1]):
        if not is_col_used[c]:
            is_col_used[c] = True
            M_copy[current_row] = np.zeros(M_copy.shape[1])
            if M0[current_row][c] == 1:
                M_copy[current_row][c] = 1
            else:
                continue

            no_recursion = m_matrix_variations1(M_copy, P, G, M0, current_row + 1, is_col_used, valid_variations,
                                                no_recursion + 1)

            is_col_used[c] = False

    return no_recursion


def m_matrix_variations(M: np.ndarray, P: np.ndarray, G: np.ndarray, M0: np.ndarray, current_row: int = 0,
                        is_col_used: np.ndarray = None, valid_variations: List = None, no_recursion: int = 0):
    if valid_variations is None:
        valid_variations = []

    if is_col_used is None:
        is_col_used = np.array([False for _ in range(M.shape[1])])

    if current_row == M.shape[0]:
        if np.array_equal(P, M @ (M @ G).T):
            valid_variations.append(M)

        return no_recursion

    M_copy = deepcopy(M)
    was_change = False
    if current_row == M_copy.shape[0] - 1:
        was_change = prune(M_copy, P, G)
    for c in range(M_copy.shape[1]):
        if was_change and current_row != 0:
            break
        if not is_col_used[c]:
            is_col_used[c] = True
            M_copy[current_row] = np.zeros(M_copy.shape[1])
            if M0[current_row][c] == 1:
                M_copy[current_row][c] = 1
            else:
                continue

            no_recursion = m_matrix_variations(M_copy, P, G, M0, current_row + 1, is_col_used, valid_variations,
                                               no_recursion + 1)

            is_col_used[c] = False

    return no_recursion


def ullman2(graph1: AdjMatrixGraph, graph2: AdjMatrixGraph):
    G: np.ndarray = graph1.get_matrix()
    P: np.ndarray = graph2.get_matrix()

    M = np.zeros((graph2.order(), graph1.order()))
    M0 = m0_matrix(P, G)

    M_variations = []
    no_recursion = m_matrix_variations1(M, P, G, M0, valid_variations=M_variations)

    return no_recursion, len(M_variations)


def ullman1(graph1: AdjMatrixGraph, graph2: AdjMatrixGraph):
    G: np.ndarray = graph1.get_matrix()
    P: np.ndarray = graph2.get_matrix()

    M = np.zeros((graph2.order(), graph1.order()))
    M0 = np.ones(M.shape)

    M_variations = []
    no_recursion = m_matrix_variations1(M, P, G, M0, valid_variations=M_variations)

    return no_recursion, len(M_variations)


def ullman(graph1: AdjMatrixGraph, graph2: AdjMatrixGraph):
    G: np.ndarray = graph1.get_matrix()
    P: np.ndarray = graph2.get_matrix()

    M = np.zeros((graph2.order(), graph1.order()))
    M0 = m0_matrix(P, G)

    M_variations = []
    no_recursion = m_matrix_variations(M, P, G, M0, valid_variations=M_variations)

    return no_recursion, len(M_variations)


def main():
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]

    p_graph = AdjMatrixGraph()
    g_graph = AdjMatrixGraph()

    vertexes_p = ['A', 'B', 'C']
    vertexes_g = ['A', 'B', 'C', 'D', 'E', 'F']

    for vertex in vertexes_p:
        p_graph.insert_vertex(Vertex(vertex))

    for key_1, key_2, weight in graph_P:
        p_graph.insert_edge(Vertex(key_1), Vertex(key_2), weight)

    for vertex in vertexes_g:
        g_graph.insert_vertex(Vertex(vertex))

    for key_1, key_2, weight in graph_G:
        g_graph.insert_edge(Vertex(key_1), Vertex(key_2), weight)

    print(ullman1(g_graph, p_graph))
    print(ullman2(g_graph, p_graph))
    print(ullman(g_graph, p_graph))


if __name__ == "__main__":
    main()
