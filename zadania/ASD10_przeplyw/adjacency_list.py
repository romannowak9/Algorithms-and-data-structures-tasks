from typing import Dict, List, Union, Tuple, Optional
from graph import Vertex, Graph, Edge
import numpy as np


class AdjListGraph(Graph):
    def __init__(self):
        super().__init__()
        self.__adj_list: List[List[Tuple[int, Edge]]] = []

    def is_empty(self) -> bool:
        return True if not self.__adj_list else False

    def insert_vertex(self, vertex: Vertex):
        order = self.order()
        self._vertex_idx[vertex] = order
        self._vertexes.append(vertex)
        self.__adj_list.append([])

    def insert_edge(self, vertex1: Vertex, vertex2: Vertex, edge: Edge):
        self.__adj_list[self.get_vertex_idx(vertex1)].append((self.get_vertex_idx(vertex2), edge))
        # Ford-Fulkerson
        self.__adj_list[self.get_vertex_idx(vertex2)].append((self.get_vertex_idx(vertex1), Edge(edge.capacity,
                                                                                                 is_residual=True)))

    def delete_vertex(self, vertex: Vertex):
        del_idx = self.get_vertex_idx(vertex)
        self.__adj_list.pop(del_idx)
        del self._vertex_idx[vertex]
        self._vertexes.pop(del_idx)

        for neighbours in self.__adj_list:
            was_del_idx = False
            v_idx_to_update = []
            for neighbour_idx, _ in neighbours:
                if neighbour_idx == del_idx:
                    was_del_idx = True
                elif neighbour_idx > del_idx:
                    v_idx_to_update.append(neighbour_idx)

            if was_del_idx:
                for i, (neighbour_idx, _) in enumerate(neighbours):
                    if neighbour_idx == del_idx:
                        neighbours.pop(i)

            for v_idx in v_idx_to_update:
                neighbours[v_idx - 1] = neighbours.pop(v_idx)

        for ver in self._vertex_idx:
            if self.get_vertex_idx(ver) > del_idx:
                self._vertex_idx[ver] -= 1

    def delete_edge(self, vertex1: Vertex, vertex2: Vertex):
        v1_idx = self.get_vertex_idx(vertex1)
        v2_idx = self.get_vertex_idx(vertex2)

        for i, (neighbour_idx, edge) in enumerate(self.__adj_list[v1_idx]):
            if neighbour_idx == v2_idx and not edge.is_residual:
                self.__adj_list[v1_idx].pop(i)

        for i, (neighbour_idx, edge) in enumerate(self.__adj_list[v2_idx]):
            if neighbour_idx == v1_idx and edge.is_residual:
                self.__adj_list[v2_idx].pop(i)

    def get_vertex_idx(self, vertex: Vertex) -> int:
        return self._vertex_idx[vertex]

    def get_vertex(self, vertex_idx: int) -> Vertex:
        return self._vertexes[vertex_idx]

    def get_edge(self, vertex1: Vertex, vertex2: Vertex, is_residual: bool = False) -> Optional[Edge]:
        v1_idx = self.get_vertex_idx(vertex1)
        v2_idx = self.get_vertex_idx(vertex2)
        for neighbour_idx, edge in self.__adj_list[v1_idx]:
            if neighbour_idx == v2_idx and is_residual == edge.is_residual:
                return edge

        return None

    def set_edge(self, vertex1: Vertex, vertex2: Vertex, edge_parameter: str, value, is_residual: bool = False) -> None:
        v1_idx = self.get_vertex_idx(vertex1)
        v2_idx = self.get_vertex_idx(vertex2)
        for neighbour_idx, edge in self.__adj_list[v1_idx]:
            if neighbour_idx == v2_idx and is_residual == edge.is_residual:
                if edge_parameter == "flow":
                    edge.flow += value
                elif edge_parameter == "residual":
                    edge.residual += value
                else:
                    raise ValueError("Wrong edge parameter!")

    def neighbours_idx(self, vertex_idx: int) -> List[int]:
        return [idx for idx, _ in self.__adj_list[vertex_idx]]

    def order(self):
        """ Liczba węzłów """
        return len(self.__adj_list)

    def size(self):
        """ Liczba krawędzi """
        size = 0
        for neighbours in self.__adj_list:
            size += len(neighbours)

        return size

    def get_vertex_parents(self, vertex: Vertex) -> List[Vertex]:
        parents = []
        vertex_idx = self.get_vertex_idx(vertex)
        for idx, neighbours in enumerate(self.__adj_list):
            for neighbour_idx, _ in neighbours:
                if neighbour_idx == vertex_idx:
                    parents.append(self.get_vertex(idx))

        return parents

    def edges(self):
        edges = []
        for idx, neighbours in enumerate(self.__adj_list):
            v1 = self.get_vertex(idx)
            for neighbour_idx, _ in neighbours:
                v2 = self.get_vertex(neighbour_idx)
                edges.append((v1.key, v2.key, self.get_edge(v1, v2)))

        return edges

    def get_vertex_edges(self, vertex: Vertex) -> List[Tuple[Vertex, Edge]]:
        edges = []
        idx = self.get_vertex_idx(vertex)
        for neighbour_idx, _ in self.__adj_list[idx]:
            v2 = self.get_vertex(neighbour_idx)
            edge = self.get_edge(vertex, v2, False)
            if edge is None:
                edge = self.get_edge(vertex, v2, True)

            edges.append((v2, edge))

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
                    for neighbour_idx, _ in self.__adj_list[self.get_vertex_idx(v)]:
                        vertexes.insert(0, self.get_vertex(neighbour_idx))

        return visited

    def bfs(self, start_vertex: Vertex) -> List[Optional[Vertex]]:
        order = self.order()
        visited = np.array([False for _ in range(order)])
        parent = [None for _ in range(order)]
        vertexes = [start_vertex]
        visited[self.get_vertex_idx(start_vertex)] = True
        while vertexes:
            v = vertexes.pop(0)
            for neighbour_idx in self.neighbours_idx(self.get_vertex_idx(v)):
                neighbour = self.get_vertex(neighbour_idx)
                edge = self.get_edge(v, neighbour, False)
                if edge is None:
                    continue
                if not visited[neighbour_idx] and edge.residual > 0:  # Niestandardowy warunek!
                    vertexes.append(neighbour)
                    visited[neighbour_idx] = True
                    parent[neighbour_idx] = v

        return parent


def print_graph(g):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.get_vertex(i)
        print(v, end=" -> ")
        nbrs = g.get_vertex_edges(v)
        for (j, w) in nbrs:
            print(j, w, end=";")
        print()
    print("-------------------")
