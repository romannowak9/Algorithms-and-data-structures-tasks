
def selection_sort_2(tab):
    size = len(tab)
    for i in range(size):
        min_el = tab[i]
        min_idx = i
        for j in range(i + 1, size):
            min_el, min_idx = (tab[j], j) if tab[j] < min_el else (min_el, min_idx)

        tab[min_idx], tab[i] = tab[i], tab[min_idx]


def selection_sort(tab):
    for i in range(len(tab)):
        tab0 = tab[i:]
        min_i = tab0.index(min(tab0)) + i
        tab[min_i], tab[i] = tab[i], tab[min_i]