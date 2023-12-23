from typing import Dict, List, Union, Tuple
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

    def get_vertex_idx(self, vertex: Vertex) -> int:
        return self._vertex_idx[vertex]

    def get_vertex(self, vertex_idx: int) -> Vertex:
        return self._vertexes[vertex_idx]

    def get_edge_weight(self, vertex1: Vertex, vertex2: Vertex):
        key1 = self.get_vertex_idx(vertex1)
        key2 = self.get_vertex_idx(vertex2)
        if key2 in self.__adj_list[key1]:
            return self.__adj_list[key1][key2]
        else:
            return None

    def neighbours_idx(self, vertex_idx: int):
        return [idx for idx in self.__adj_list[vertex_idx]]

    def order(self):
        """ Liczba węzłów """
        return len(self.__adj_list)

    def size(self):
        """ Liczba krawędzi """
        size = 0
        for neighbours in self.__adj_list:
            size += len(neighbours)

        return size

    def edges(self):
        edges = []
        for idx, neighbours in enumerate(self.__adj_list):
            v1 = self.get_vertex(idx)
            for neighbour in neighbours:
                v2 = self.get_vertex(neighbour)
                edges.append((v1.key, v2.key, self.get_edge_weight(v1, v2)))

        return edges

    def get_vertex_edges(self, vertex: Vertex) -> List[Tuple[Vertex, Union[float, int]]]:
        edges = []
        idx = self.get_vertex_idx(vertex)
        for neighbour in self.__adj_list[idx]:
            v2 = self.get_vertex(neighbour)
            edges.append((v2, self.get_edge_weight(vertex, v2)))

        return edges

    def is_vertex_in_graph(self, vertex: Vertex):
        return True if vertex in self._vertexes else False

    def dfs(self, start_vertex: Vertex) -> List[Vertex]:
        visited: List[Vertex] = []
        vertexes: List[Vertex] = [start_vertex]
        while vertexes:
            v = vertexes.pop(-1)
            if v not in visited:
                visited.append(v)
                if v in self._vertexes:
                    for neighbour in self.__adj_list[self.get_vertex_idx(v)]:
                        vertexes.insert(0, self.get_vertex(neighbour))

        return visited

