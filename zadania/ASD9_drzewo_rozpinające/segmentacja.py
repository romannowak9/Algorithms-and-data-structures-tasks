import cv2
from adjacency_list import AdjListGraph
from min_spanning_tree import prim_min_spanning_tree, print_graph
from graph import Vertex
import numpy as np
import matplotlib.pyplot as plt


def segmentation(img):
    graph1 = AdjListGraph()
    YY = img.shape[0]
    XX = img.shape[1]
    for j in range(YY):
        for i in range(XX):
            graph1.insert_vertex(Vertex(XX * j + i))

    for j in range(0, YY):
        for i in range(0, XX):
            current_v = Vertex(XX * j + i)
            for m in range(i - 1, i + 2):
                for k in range(j - 1, j + 2):
                    if (k != j or m != i) and YY > k >= 0 and XX > m >= 0:
                        graph1.insert_edge(current_v, Vertex(XX * k + m), np.abs(img[j, i] - img[m, k]))

    mst = prim_min_spanning_tree(graph1)
    #print_graph(graph1)
    edges_list = mst.edges()
    weights = [el[2] for el in edges_list]
    max_v1, max_v2, _ = edges_list[weights.index(max(weights))]

    mst.delete_edge(mst.get_vertex(max_v1), mst.get_vertex(max_v2))

    img_wy = np.zeros((YY, XX), dtype='uint8')

    tree1_vertexes = mst.dfs(mst.get_vertex(max_v1))
    tree2_vertexes = mst.dfs(mst.get_vertex(max_v2))

    print(tree1_vertexes)
    print(tree2_vertexes)

    for v in tree1_vertexes:
        img_wy[v.key // XX, v.key % XX] = 100

    for v in tree2_vertexes:
        img_wy[v.key // XX, v.key % XX] = 200

    return img_wy


def main():
    sample = cv2.imread("sample.png", cv2.IMREAD_GRAYSCALE)

    seg_img = segmentation(sample)

    plt.imshow(seg_img, "gray", vmin=0, vmax=255)
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()
