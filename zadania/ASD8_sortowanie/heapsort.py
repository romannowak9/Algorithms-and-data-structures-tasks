from heap import Heap, HeapElem
import random
import time
from selection_sort import *


def main():
    tab1 = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    tab_to_sort = [HeapElem(priority, data) for priority, data in tab1]

    heap1 = Heap(tab_to_sort)

    heap1.print_tab()
    heap1.print_tree()

    heap1.sort()
    heap1.print_tab()

    rand_tab = [int(random.random() * 100) for _ in range(10000)]

    t_start = time.perf_counter()
    heap2 = Heap(rand_tab)
    heap2.sort()
    t_stop = time.perf_counter()
    print("Czas obliczeń dla sortowania przez kopcowanie:", "{:.7f}".format(t_stop - t_start))

    tab_to_sort3 = [HeapElem(priority, data) for priority, data in tab1]
    selection_sort(tab_to_sort3)
    print(tab_to_sort3)

    rand_tab2 = [int(random.random() * 100) for _ in range(1000)]
    rand_tab3 = rand_tab2.copy()

    t_start = time.perf_counter()
    selection_sort_2(rand_tab2)
    t_stop = time.perf_counter()

    t_start_2 = time.perf_counter()
    selection_sort(rand_tab3)
    t_stop_2 = time.perf_counter()

    print("Czas obliczeń dla sortowania przez wybieranie:", "{:.7f}".format(t_stop - t_start))
    print("Czas obliczeń dla sortowania przez wybieranie:", "{:.7f}".format(t_stop_2 - t_start_2))


if __name__ == "__main__":
    main()
