from typing import Union, Optional
from graph import Vertex, Graph
import numpy as np


class AdjMatrixGraph(Graph):
    def __init__(self, init_value=0):
        super().__init__()
        self.__matrix = np.empty((0, 0))
        self.__init_value = init_value

    def get_matrix(self):
        return self.__matrix

    def is_empty(self) -> bool:
        return True if not self.__matrix else False

    def insert_vertex(self, vertex: Vertex):
        order = self.order()
        self._vertex_idx[vertex] = order
        self._vertexes.append(vertex)
        col = np.empty(order)
        col.fill(self.__init_value)
        self.__matrix = np.c_[self.__matrix, col]
        row = np.empty(order + 1)
        row.fill(self.__init_value)
        self.__matrix = np.r_[self.__matrix, [row]]

    def insert_edge(self, vertex1: Vertex, vertex2: Vertex, edge: Union[int, float] = 1):
        self.__matrix[self.get_vertex_idx(vertex1), self.get_vertex_idx(vertex2)] = edge
        # Graf nieskierowany
        self.__matrix[self.get_vertex_idx(vertex2), self.get_vertex_idx(vertex1)] = edge

    def delete_vertex(self, vertex: Vertex):
        del_idx = self.get_vertex_idx(vertex)
        self.__matrix = np.delete(self.__matrix, del_idx, axis=0)
        self.__matrix = np.delete(self.__matrix, del_idx, axis=1)
        del self._vertex_idx[vertex]
        self._vertexes.pop(del_idx)

        for ver in self._vertex_idx:
            if self.get_vertex_idx(ver) > del_idx:
                self._vertex_idx[ver] -= 1

    def delete_edge(self, vertex1: Vertex, vertex2: Vertex):
        self.__matrix[self.get_vertex_idx(vertex1), self.get_vertex_idx(vertex2)] = self.__init_value
        # Graf nieskierowany, więc w dwie strony
        self.__matrix[self.get_vertex_idx(vertex2), self.get_vertex_idx(vertex1)] = self.__init_value

    def get_vertex_idx(self, vertex: Vertex) -> int:
        return self._vertex_idx[vertex]

    def get_vertex(self, vertex_idx: int) -> Vertex:
        return self._vertexes[vertex_idx]

    def neighbours_idx(self, vertex_idx: int):
        return [idx for idx, value in enumerate(self.__matrix[vertex_idx]) if value != self.__init_value]

    def order(self):
        '''Liczba wierzchołków'''
        return self.__matrix.shape[0]

    def size(self):
        '''Liczba krawędzi'''
        size = 0
        for row in self.__matrix:
            for edge in row:
                if edge != self.__init_value:
                    size += 1

        return size // 2  # Graf nieskierowany i bez pętli

    def edges(self):
        # Dla grafu nieskierowanego
        order = self.order()
        return [(self.get_vertex(j).key, self.get_vertex(i).key) for i in range(order)
                for j in range(i, order) if self.__matrix[i][j] != self.__init_value]
