from typing import Any, List


class HeapElem:
    def __init__(self, data: Any, priority: int):
        self.__data = data
        self.__priority = priority

    def __lt__(self, other) -> bool:
        if self.__priority < other.__priority:
            return True
        else:
            return False

    def __gt__(self, other) -> bool:
        if self.__priority > other.__priority:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"{self.__priority} : {self.__data}.\n"


class Heap:
    def __init__(self):
        self.__tab: List[HeapElem] = []
        self.__heap_size: int = 0
        self.__tab_size: int = 0

    def is_empty(self):
        return True if self.__heap_size == 0 else False

    def peek(self):
        return self.__tab[0] if not self.is_empty() else None

    def enqueue(self, elem: HeapElem):
        if self.__tab_size == self.__heap_size:
            self.__tab.append(elem)
        else:
            self.__tab[self.__heap_size] = elem

        self.__repair_prev(self.__heap_size)

        self.__heap_size += 1
        self.__tab_size += 1

    def dequeue(self):
        el = self.__tab[0]
        self.__tab[0], self.__tab[self.__heap_size - 1] = self.__tab[self.__heap_size - 1], self.__tab[0]
        self.__heap_size -= 1
        self.__repair_next(0)

        return el

    def print_tab(self):
        print('{', end=' ')
        print(*self.__tab[:self.__heap_size], sep=', ', end=' ')
        print('}')

    def print_tree(self, idx, lvl):
        if idx < self.__heap_size:
            if self.__right(idx) is not None:
                self.print_tree(self.__right(idx), lvl + 1)
            print(2 * lvl * '  ', self.__tab[idx] if self.__tab[idx] else None)
            if self.__left(idx) is not None:
                self.print_tree(self.__left(idx), lvl + 1)

    def __repair_prev(self, idx):
        if self.__parent(idx) is None:
            return None

        if self.__tab[idx] > self.__tab[self.__parent(idx)]:
            self.__tab[idx], self.__tab[self.__parent(idx)] = self.__tab[self.__parent(idx)], self.__tab[idx]
            return self.__repair_prev(self.__parent(idx))
        else:
            return None

    def __repair_next(self, idx):
        if self.__left(idx) is None and self.__right(idx) is None:
            return None
        elif self.__right(idx) is None:
            if self.__tab[idx] < self.__tab[self.__left(idx)]:
                self.__tab[idx], self.__tab[self.__left(idx)] = self.__tab[self.__left(idx)], self.__tab[idx]

            return None

        if self.__tab[idx] < self.__tab[self.__right(idx)] or self.__tab[idx] < self.__tab[self.__left(idx)]:
            if self.__tab[self.__right(idx)] > self.__tab[self.__left(idx)]:
                self.__tab[idx], self.__tab[self.__right(idx)] = self.__tab[self.__right(idx)], self.__tab[idx]
                return self.__repair_next(self.__right(idx))
            else:
                self.__tab[idx], self.__tab[self.__left(idx)] = self.__tab[self.__left(idx)], self.__tab[idx]
                return self.__repair_next(self.__left(idx))
        else:
            return None

    def __left(self, idx):
        return 2 * idx + 1 if self.__heap_size > 2 * idx + 1 else None

    def __right(self, idx):
        return 2 * idx + 2 if self.__heap_size > 2 * idx + 2 else None

    def __parent(self, idx):
        return (idx - 1) // 2 if idx > 0 else None


def main():
    heap1 = Heap()
    p = [7, 5, 1, 2, 5, 3, 4, 8, 9]
    text = "GRYMOTYLA"

    for i, el in enumerate(p):
        heap1.enqueue(HeapElem(data=text[i], priority=el))

    heap1.print_tree(0, 0)
    heap1.print_tab()

    root = heap1.dequeue()
    print(heap1.peek())

    heap1.print_tab()

    print(root)

    while not heap1.is_empty():
        print(heap1.dequeue())

    heap1.print_tab()

    list1 = ["a", "b", "c", "d", "e"]
    for i, el in enumerate(list1[2:]):
        print(i, el)


if __name__ == "__main__":
    main()
