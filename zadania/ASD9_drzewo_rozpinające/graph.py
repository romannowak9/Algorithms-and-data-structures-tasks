from abc import ABC, abstractmethod
from typing import Dict, List


class Vertex:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data

    def __eq__(self, other):
        return True if self.key == other.key else False

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return str(self.key)


class Graph(ABC):
    def __init__(self):
        super().__init__()
        self._vertex_idx: Dict = {}
        self._vertexes: List[Vertex] = []

    @abstractmethod
    def is_empty(self):
        raise NotImplementedError()

    @abstractmethod
    def insert_vertex(self, vertex):
        raise NotImplementedError()

    @abstractmethod
    def insert_edge(self, vertex1, vertex2, edge=1):
        raise NotImplementedError()

    @abstractmethod
    def delete_vertex(self, vertex):
        raise NotImplementedError()

    @abstractmethod
    def delete_edge(self, vertex1, vertex2):
        raise NotImplementedError()

    @abstractmethod
    def get_vertex_idx(self, vertex):
        raise NotImplementedError()

    @abstractmethod
    def get_vertex(self, vertex_idx):
        raise NotImplementedError()

    @abstractmethod
    def neighbours_idx(self, vertex_idx):
        raise NotImplementedError()

    @abstractmethod
    def order(self):
        raise NotImplementedError()

    @abstractmethod
    def size(self):
        raise NotImplementedError()

    @abstractmethod
    def edges(self):
        raise NotImplementedError()
