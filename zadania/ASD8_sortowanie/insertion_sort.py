import random
import time

from heap import HeapElem


def insertion_sort(tab):
    for i in range(1, len(tab)):
        insert_elem = tab[i]
        j = i - 1
        while j >= 0 and tab[j] > insert_elem:
            tab[j + 1] = tab[j]
            j -= 1

        tab[j + 1] = insert_elem


def shell_sort(tab):
    n = len(tab)
    h = n // 2

    while h > 0:
        for j in range(h, n):
            i = j - h
            while i >= 0 and tab[i + h] < tab[i]:
                tab[i + h], tab[i] = tab[i], tab[i + h]

                i -= h

        h = h // 2


def main():
    tab1 = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    tab_to_sort = [HeapElem(priority, data) for priority, data in tab1]

    insertion_sort(tab_to_sort)
    print(tab_to_sort)

    rand_tab = [int(random.random() * 100) for _ in range(10000)]

    t_start = time.perf_counter()
    insertion_sort(rand_tab)
    t_stop = time.perf_counter()
    print("Czas obliczeń dla sortowania przez wstawianie:", "{:.7f}".format(t_stop - t_start))

    tab_to_sort3 = [HeapElem(priority, data) for priority, data in tab1]
    shell_sort(tab_to_sort3)
    print(tab_to_sort3)

    rand_tab2 = [int(random.random() * 100) for _ in range(10000)]

    t_start = time.perf_counter()
    shell_sort(rand_tab2)
    t_stop = time.perf_counter()

    print("Czas obliczeń dla sortowania przez wybieranie:", "{:.7f}".format(t_stop - t_start))


if __name__ == "__main__":
    main()
