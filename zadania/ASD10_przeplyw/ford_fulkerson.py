from typing import List, Optional, Tuple

from graph import Vertex, Edge
from adjacency_list import AdjListGraph, print_graph


def find_min_capacity(graph0: AdjListGraph, start_vertex: Vertex,
                      end_vertex: Vertex, parent: List[Optional[Vertex]]) -> float:
    current_v_idx = graph0.get_vertex_idx(end_vertex)
    min_capacity = float('inf')

    if not parent[current_v_idx]:
        return 0

    start_v_idx = graph0.get_vertex_idx(start_vertex)
    while current_v_idx != start_v_idx:
        current_v = graph0.get_vertex(current_v_idx)
        # Krawędź rzeczywista
        edge: Edge = graph0.get_edge(parent[current_v_idx], current_v)
        if edge.residual < min_capacity:
            min_capacity = edge.residual

        current_v_idx = graph0.get_vertex_idx(parent[current_v_idx])

    return min_capacity


def path_aug(graph0: AdjListGraph, start_vertex: Vertex, end_vertex: Vertex,
             parent: List[Optional[Vertex]], min_capacity: float) -> None:
    current_v_idx = graph0.get_vertex_idx(end_vertex)
    start_v_idx = graph0.get_vertex_idx(start_vertex)
    while current_v_idx != start_v_idx:
        current_v = graph0.get_vertex(current_v_idx)
        # Krawędź rzeczywista
        graph0.set_edge(parent[current_v_idx], current_v, "flow", min_capacity, False)
        graph0.set_edge(parent[current_v_idx], current_v, "residual", -min_capacity, False)
        # Krawędź resztowa
        graph0.set_edge(current_v, parent[current_v_idx], "residual", min_capacity, True)

        current_v_idx = graph0.get_vertex_idx(parent[current_v_idx])


def ford_fulkerson(graph0: AdjListGraph, start_vertex: Vertex, end_vertex: Vertex):
    parent = graph0.bfs(start_vertex)
    min_capacity = find_min_capacity(graph0, start_vertex, end_vertex, parent)
    while min_capacity > 0:
        path_aug(graph0, start_vertex, end_vertex, parent, min_capacity)
        parent = graph0.bfs(start_vertex)
        min_capacity = find_min_capacity(graph0, start_vertex, end_vertex, parent)

    end_v_parents = graph0.get_vertex_parents(end_vertex)

    return sum([graph0.get_edge(v, end_vertex).flow for v in end_v_parents])


def graph_from_edges(edges_list: List[Tuple]) -> AdjListGraph:
    vertexes = list(set([key_1 for key_1, _, _ in edges_list]).union(set([key_2 for _, key_2, _ in edges_list])))
    graph1 = AdjListGraph()

    for vertex in vertexes:
        graph1.insert_vertex(Vertex(vertex))

    for key_1, key_2, capacity in edges_list:
        graph1.insert_edge(Vertex(key_1), Vertex(key_2), Edge(capacity))

    return graph1


def main():
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
              ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
              ('d', 'c', 4)]

    graph0 = graph_from_edges(graf_0)

    print(ford_fulkerson(graph0, Vertex('s'), Vertex('t')))
    print_graph(graph0)

    graph1 = graph_from_edges(graf_1)

    print(ford_fulkerson(graph1, Vertex('s'), Vertex('t')))
    print_graph(graph1)

    graph2 = graph_from_edges(graf_2)

    print(ford_fulkerson(graph2, Vertex('s'), Vertex('t')))
    print_graph(graph2)

    graph3 = graph_from_edges(graf_3)

    print(ford_fulkerson(graph3, Vertex('s'), Vertex('t')))
    print_graph(graph3)


if __name__ == "__main__":
    main()
