# maksymalna liczba elementów w węźle jest nieparzysta (a więc pełny węzeł ma parzystą liczbę potomków).
# dodawanymi elementami będą same klucze (pomijamy dane, które zazwyczaj towarzyszą kluczom)
# w wypadku gdy węzeł, do którego ma być dodany element jest pełny, następuje jego podział
# (nie ma próby przesunięcia elementów do sąsiednich węzłów)
# nie sprawdzamy czy próbujemy wstawić już istniejący klucz
from typing import List, Optional, Tuple


class BTreeElem:
    def __init__(self, k):
        self.keys: List[int] = []
        self.children: List[BTreeElem] = []
        if k % 2:  # Założenie
            raise ValueError("Maximum quantity of children must be even!")

        self.k = k

    def insert(self, key, new_node=None):
        n_node = None
        mid_key = None
        if self.is_full():  # Podział
            mid_idx = self.k // 2 - 1
            n_node = BTreeElem(self.k)
            mid_key = self.keys.pop(mid_idx)
            for i in range(len(self.keys[mid_idx:])):
                n_node.keys.insert(i, self.keys.pop(mid_idx))

            for i in range(len(self.children[mid_idx + 1:])):
                n_node.children.insert(i, self.children.pop(mid_idx))

        was_break = False
        for i, node_key in enumerate(self.keys):
            if node_key > key:
                self.keys.insert(i, key)
                if new_node is not None:
                    self.children.insert(i, key)
                was_break = True
                break

        if n_node is not None and not was_break:
            for i, node_key in enumerate(n_node.keys):
                if node_key > key:
                    n_node.keys.insert(i, key)
                    if new_node is not None:
                        self.children.insert(i, key)
                    break

        if not self.keys:
            self.keys.append(key)

        return mid_key, n_node

    def get(self, idx):
        return self.keys[idx]

    def is_leaf(self):
        return True if not self.children else False

    def is_full(self):
        return True if self.k == len(self.keys) - 1 else False

    def size(self):
        return len(self.keys)


class BTree:
    def __init__(self, k: int):
        self.root = None
        if k % 2:  # Założenie
            raise ValueError("Maximum quantity of children must be even!")

        self.k = k

    def insert(self, key: int, node: Optional[BTreeElem] = None) -> Tuple[Optional[int], Optional[BTreeElem]]:
        if self.root is None:
            self.root = BTreeElem(self.k)

        if node is None:
            node = self.root

        was_break = False
        mid_key, new_elem = None, None
        for idx, node_key in enumerate(node.keys):
            if node_key > key:
                if node.is_leaf():
                    mid_key, new_elem = node.insert(key)
                else:
                    mid_key, new_elem = self.insert(key, node.children[idx])  # Lewy potomek znalezionego klucza

                was_break = True
                break

        if not was_break and not node.is_leaf():  # Wstawiany klucz jest większy od wszystkich w węźle
            mid_key, new_elem = self.insert(key, node.children[-1])
        elif not was_break:
            node.insert(key)

        if mid_key is not None:  # Doszło do podziału
            mid_key, new_elem = node.insert(mid_key, new_elem)

        # Czy nastąpił podział roota
        if mid_key is not None and node == self.root:
            new_root = BTreeElem(self.k)
            new_root.keys.append(mid_key)
            new_root.children.append(self.root)
            new_root.children.append(new_elem)
            self.root = new_root

        return mid_key, new_elem

    def print_tree(self):
        print("==============")
        self.__print_tree(self.root, 0)
        print("==============")

    def __print_tree(self, node, lvl):
        if not node.is_leaf():
            for i, child in enumerate(node.children):
                self.__print_tree(child, lvl + 1)

            for key in node.keys:
                print(lvl * '  ', key)
        else:
            for key in node.keys:
                print(lvl * '  ', key)


def main():
    tree = BTree(k=4)
    keys = [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]
    for key in keys:
        tree.insert(key)
        tree.print_tree()


if __name__ == "__main__":
    main()
