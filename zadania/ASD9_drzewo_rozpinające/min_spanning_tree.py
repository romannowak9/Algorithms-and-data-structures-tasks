from graph import Vertex
from adjacency_list import AdjListGraph
from graf_mst import graf


def prim_min_spanning_tree(graph: AdjListGraph):
    order = graph.order()
    intree = [0 for _ in range(order)]
    distance = [float('inf') for _ in range(order)]
    parent = [-1 for _ in range(order)]

    # Tworzę graf o tych samych wierzchołkach, bez krawędzi
    span_tree = AdjListGraph()
    for current_v_idx in range(order):
        span_tree.insert_vertex(graph.get_vertex(current_v_idx))

    v_idx = 0
    while intree[v_idx] == 0:
        intree[v_idx] = 1

        v_edges = graph.get_vertex_edges(graph.get_vertex(v_idx))
        for neighbour, weight in v_edges:
            neighbour_idx = graph.get_vertex_idx(neighbour)
            if weight < distance[neighbour_idx] and not intree[neighbour_idx]:
                distance[neighbour_idx] = weight
                parent[neighbour_idx] = v_idx

        # Przegląd po wszystkich wierzchołkach (po indeksach)
        new_v_idx = 0
        for current_v_idx in range(order):
            if not intree[current_v_idx] and distance[current_v_idx] <= distance[new_v_idx]:
                new_v_idx = current_v_idx

        if distance[new_v_idx] != float('inf'):
            span_tree.insert_edge(span_tree.get_vertex(new_v_idx),
                                  span_tree.get_vertex(parent[new_v_idx]), distance[new_v_idx])
            span_tree.insert_edge(span_tree.get_vertex(parent[new_v_idx]),
                                  span_tree.get_vertex(new_v_idx), distance[new_v_idx])

        v_idx = new_v_idx

    return span_tree


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


def main():
    vertexes = list(set([key_1 for key_1, _, _ in graf]).union(set([key_2 for _, key_2, _ in graf])))
    graph1 = AdjListGraph()

    for vertex in vertexes:
        graph1.insert_vertex(Vertex(vertex))

    for key_1, key_2, weight in graf:
        graph1.insert_edge(Vertex(key_1), Vertex(key_2), weight)
        graph1.insert_edge(Vertex(key_2), Vertex(key_1), weight)

    min_span_tree = prim_min_spanning_tree(graph1)

    print_graph(min_span_tree)


if __name__ == "__main__":
    main()
