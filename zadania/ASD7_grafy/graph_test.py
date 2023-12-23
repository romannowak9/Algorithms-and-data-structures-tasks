from adjacency_matrix import AdjMatrixGraph
from adjacency_list import AdjListGraph
from polska import graf as edges, draw_map
from graph import Vertex


def main():
    vertexes = {'Z': Vertex('Z'), 'G': Vertex('G'), 'N': Vertex('N'), 'B': Vertex('B'), 'F': Vertex('F'),
                'P': Vertex('P'), 'C': Vertex('C'), 'W': Vertex('W'), 'L': Vertex('L'), 'D': Vertex('D'),
                'O': Vertex('O'), 'E': Vertex('E'), 'S': Vertex('S'), 'T': Vertex('T'), 'K': Vertex('K'),
                'R': Vertex('R')}

    graph1 = AdjMatrixGraph()
    graph2 = AdjListGraph()

    for key in vertexes:
        graph1.insert_vertex(vertexes[key])
        graph2.insert_vertex(vertexes[key])

    for edge in edges:
        graph1.insert_edge(vertexes[edge[0]], vertexes[edge[1]])
        graph2.insert_edge(vertexes[edge[0]], vertexes[edge[1]])

    graph1.delete_vertex(vertexes['K'])
    graph1.delete_edge(vertexes['W'], vertexes['E'])

    graph2.delete_vertex(vertexes['K'])
    graph2.delete_edge(vertexes['W'], vertexes['E'])

    # print([graph2.get_vertex(el).key for el in graph2.neighbours_idx(graph2.get_vertex_idx(vertexes['E']))], end=" ")
    draw_map(graph1.edges())
    # Żeby zobaczyć działanie graph2, zakomentować powyższą linijkę
    draw_map(graph2.edges())


if __name__ == "__main__":
    main()
