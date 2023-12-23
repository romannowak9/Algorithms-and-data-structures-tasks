from typing import List, Tuple
from matplotlib import pyplot as plt
from graph import Vertex, Edge
from adjacency_list import AdjListGraph, print_graph
import numpy as np
import cv2
from ford_fulkerson import ford_fulkerson


def min_cut(residual_graph: AdjListGraph, start_vertex: Vertex, end_vertex: Vertex) -> List[Tuple[Vertex, Vertex]]:
    parent: List[Vertex] = residual_graph.bfs(start_vertex)
    min_cut_edges: List[Tuple[Vertex, Vertex]] = []
    if parent[residual_graph.get_vertex_idx(end_vertex)] is None:  # Brak ścieżki z s do t
        for neighbour_idx in residual_graph.neighbours_idx(residual_graph.get_vertex_idx(start_vertex)):
            neighbour = residual_graph.get_vertex(neighbour_idx)
            edge = residual_graph.get_edge(start_vertex, neighbour, is_residual=False)
            if edge is not None:  # Tylko krawędzie nie rezydualne
                min_cut_edges.append((start_vertex, neighbour))

        return min_cut_edges

    for v in parent:
        if v is not None:
            for neighbour_idx in residual_graph.neighbours_idx(residual_graph.get_vertex_idx(v)):
                neighbour = residual_graph.get_vertex(neighbour_idx)
                if parent[neighbour_idx] is None:  # Tylko krawędzie prowadzące do wierzchołków nie osiągalnych
                    edge = residual_graph.get_edge(v, neighbour, is_residual=False)
                    if edge is not None and edge.flow == 0:  # Tylko krawędzie nie rezydualne o przepływie 0
                        min_cut_edges.append((v, neighbour))

    return min_cut_edges


def main():
    img = cv2.imread('min_cut_seg_1.png', cv2.IMREAD_GRAYSCALE)
    YY, XX = img.shape
    img_object = np.zeros((YY, XX), dtype=np.ubyte)
    img_object[100:120, 100:120] = 255

    img_background = np.zeros((YY, XX), dtype=np.ubyte)
    img_background[0:20, 0:20] = 255

    img = cv2.resize(img, (32, 32))
    img_background = cv2.resize(img_background, (32, 32))
    img_object = cv2.resize(img_object, (32, 32))

    hist_object = cv2.calcHist([img], [0], img_object, [256], [0, 256])
    hist_object = hist_object / sum(hist_object)

    hist_background = cv2.calcHist([img], [0], img_background, [256], [0, 256])
    hist_background = hist_background / sum(hist_background)

    YY, XX = img.shape

    graph1 = AdjListGraph()
    graph1.insert_vertex(Vertex('s'))
    graph1.insert_vertex(Vertex('t'))

    for j in range(YY):
        for i in range(XX):
            graph1.insert_vertex(Vertex(XX * j + i))

    for j in range(0, YY):
        for i in range(0, XX):
            current_v = Vertex(XX * j + i)
            for m in range(i - 1, i + 2):
                for k in range(j - 1, j + 2):
                    if (k != j or m != i) and YY > k >= 0 and XX > m >= 0:
                        graph1.insert_edge(current_v, Vertex(XX * k + m),
                                           Edge(np.exp((-0.5) * np.abs(img[j, i] - img[m, k]))))

    for j in range(0, YY):
        for i in range(0, XX):
            if img_object[j, i]:  # Piksel należy do tła
                graph1.insert_edge(Vertex('s'), Vertex(XX * j + i), Edge(float('inf')))
                graph1.insert_edge(Vertex(XX * j + i), Vertex('t'), Edge(0))
            elif img_background[j, i]:  # Piksel należy do obiektu
                graph1.insert_edge(Vertex('s'), Vertex(XX * j + i), Edge(0))
                graph1.insert_edge(Vertex(XX * j + i), Vertex('t'), Edge(float('inf')))
            else:  # Piksel nie został wcześniej oznaczony
                graph1.insert_edge(Vertex('s'), Vertex(XX * j + i), Edge(hist_object[img[j, i]]))
                graph1.insert_edge(Vertex(XX * j + i), Vertex('t'), Edge(hist_background[img[j, i]]))

    ford_fulkerson(graph1, Vertex('s'), Vertex('t'))
    edges_to_cut = min_cut(graph1, Vertex('s'), Vertex('t'))

    for v1, v2 in edges_to_cut:
        graph1.delete_edge(v1, v2)

    seg_result = np.zeros(img.shape)
    parent: List[Vertex] = graph1.bfs(Vertex('s'))
    for v in parent:
        if v is not None:
            seg_result[v.key // XX, v.key % XX] = 255

    plt.imshow(seg_result, "gray", vmin=0, vmax=255)
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()
