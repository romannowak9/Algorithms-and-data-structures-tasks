from typing import Dict, List, Union
from graph import Vertex, Graph


class AdjListGraph(Graph):
    def __init__(self):
        super().__init__()
        self.__adj_list: List[Dict] = []

    def is_empty(self) -> bool:
        return True if not self.__adj_list else False

    def insert_vertex(self, vertex: Vertex):
        order = self.order()
        self._vertex_idx[vertex] = order
        self._vertexes.append(vertex)
        self.__adj_list.append({})

    def insert_edge(self, vertex1: Vertex, vertex2: Vertex, edge: Union[int, float] = None):
        self.__adj_list[self.get_vertex_idx(vertex1)][self.get_vertex_idx(vertex2)] = edge
        # Graf nieskierowany
        self.__adj_list[self.get_vertex_idx(vertex1)][self.get_vertex_idx(vertex2)] = edge

    def delete_vertex(self, vertex: Vertex):
        del_idx = self.get_vertex_idx(vertex)
        self.__adj_list.pop(del_idx)
        del self._vertex_idx[vertex]
        self._vertexes.pop(del_idx)

        for neighbours in self.__adj_list:
            was_del_idx = False
            keys_to_update = []
            for neighbour in neighbours:
                if neighbour == del_idx:
                    was_del_idx = True
                elif neighbour > del_idx:
                    keys_to_update.append(neighbour)

            if was_del_idx:
                del neighbours[del_idx]

            for key in keys_to_update:
                neighbours[key - 1] = neighbours.pop(key)

        for ver in self._vertex_idx:
            if self.get_vertex_idx(ver) > del_idx:
                self._vertex_idx[ver] -= 1

    def delete_edge(self, vertex1: Vertex, vertex2: Vertex):
        del self.__adj_list[self.get_vertex_idx(vertex1)][self.get_vertex_idx(vertex2)]
        # Graf nieskierowany
        del self.__adj_list[self.get_vertex_idx(vertex2)][self.get_vertex_idx(vertex1)]

    def get_vertex_idx(self, vertex: Vertex) -> int:
        return self._vertex_idx[vertex]

    def get_vertex(self, vertex_idx: int) -> Vertex:
        return self._vertexes[vertex_idx]

    def neighbours_idx(self, vertex_idx: int):
        # Graf nieskierowany -> nie muszę szukać w innych węzłach
        return [idx for idx in self.__adj_list[vertex_idx]]

    def order(self):
        return len(self.__adj_list)

    def size(self):
        size = 0
        for neighbours in self.__adj_list:
            size += len(neighbours)

        return size // 2  # Graf nieskierowany i bez pętli

    def edges(self):
        edges = []
        for idx, neighbours in enumerate(self.__adj_list):
            for neighbour in neighbours:
                idx_1 = self.get_vertex(idx).key
                idx_2 = self.get_vertex(neighbour).key
                # Warunek dla grafu nieskierowanego - usuwa dupliakty
                if (idx_2, idx_1) not in edges:
                    edges.append((idx_1, idx_2))

        return edges
