from typing import Optional
import numpy as np


class Node:
    def __init__(self, key: int, value, right=None, left=None):
        self.key = key
        self.value = value
        self.right = right
        self.left = left

    def search(self, key: int):
        if self.key == key:
            return self.value
        elif key < self.key:
            if self.left is not None:
                return self.left.search(key)
            else:
                return None

        else:
            if self.right is not None:
                return self.right.search(key)
            else:
                return None

    def insert(self, key: int, value):
        if key == self.key:
            self.value = value
            return
        elif key < self.key:
            if self.left is not None:
                return self.left.insert(key, value)
            else:
                self.left = Node(key, value)
                return
        else:
            if self.right is not None:
                return self.right.insert(key, value)
            else:
                self.right = Node(key, value)
                return

    def delete(self, key: int):
        # print("key:", key, "self.left.key:", self.left.key, "self.right.key:", self.right.key)
        if self.left is not None:
            if key == self.left.key:
                # Brak dzieci
                if self.left.left is None and self.left.right is None:
                    self.left = None

                # Jedno dziecko
                elif self.left.left is None or self.left.right is None:
                    if self.left.left is not None:
                        self.left = self.left.left
                    else:
                        self.left = self.left.right

                # Oboje dzieci
                else:
                    el = self.left.right
                    if el.left is not None:
                        while el.left.left is not None:
                            el = el.left
                        least = el.left
                        self.left.value = least.value
                        self.left.key = least.key
                        el.left = least.right
                    else:
                        least = el
                        self.left.value = least.value
                        self.left.key = least.key
                        self.left.right = least.right

                return None

        if self.right is not None:
            if key == self.right.key:
                # Brak dzieci
                if self.right.left is None and self.right.right is None:
                    self.right = None

                # Jedno dziecko
                elif self.right.left is None or self.right.right is None:
                    if self.right.left is not None:
                        self.right = self.right.left
                    else:
                        self.right = self.right.right

                # Oboje dzieci
                else:
                    el = self.right.right
                    if el.left is not None:
                        while el.left.left is not None:
                            el = el.left
                        least = el.left
                        self.right.value = least.value
                        self.right.key = least.key
                        el.left = least.right
                    else:
                        least = el
                        self.right.value = least.value
                        self.right.key = least.key
                        self.right.right = least.right

                return None

        if key < self.key:
            if self.left is not None:
                return self.left.delete(key)
            else:
                # print("XD:", self.key)
                raise ValueError("Invalid key!")
        else:
            if self.right is not None:
                return self.right.delete(key)
            else:
                raise ValueError("Invalid key!")

    def height(self) -> int:
        if self is None:
            return 0

        left_branch = 1
        right_branch = 1

        if self.left is not None:
            left_branch = self.left.height() + 1

        if self.right is not None:
            right_branch = self.right.height() + 1

        return max(left_branch, right_branch)


class BSTTree:
    def __init__(self):
        self._root = None

    def is_empty(self):
        return True if self._root is None else False

    def search(self, key: int):
        if self.is_empty():
            return None
        else:
            return self._root.search(key)

    def insert(self, key: int, value):
        if self.is_empty():
            self._root = Node(key, value)
        else:
            self._root.insert(key, value)

    def delete(self, key: int):
        if self.is_empty():
            raise ValueError("Invalid key!")

        if key == self._root.key:
            # Brak dzieci
            if self._root.left is None and self._root.right is None:
                self._root = None

            # Jedno dziecko
            elif self._root.left is None or self._root.right is None:
                if self._root.left is not None:
                    self._root = self._root.left
                else:
                    self._root = self._root.right

            # Oboje dzieci
            else:
                el = self._root.right
                if el.left is not None:
                    while el.left.left is not None:
                        el = el.left
                    least = el.left
                    self._root.value = least.value
                    self._root.key = least.key
                    el.left = least.right
                else:
                    least = el
                    self._root.value = least.value
                    self._root.key = least.key
                    self._root.right = least.right

            return

        self._root.delete(key)

    def print_tree(self):
        print("==============")
        self.__print_tree(self._root, 0)
        print("==============")

    def __print_tree(self, node, lvl):
        if node is not None:
            self.__print_tree(node.right, lvl + 5)

            print()
            print(lvl * " ", node.key, node.value)

            self.__print_tree(node.left, lvl + 5)

    def __str__(self):
        sort_nodes = []
        self.__nodes_list(self._root, sort_nodes)
        s = ""
        for el in sort_nodes:
            s += f"{el[0]} {el[1]}, "

        return s[:-2] + '\n'

    def __nodes_list(self, node, sorted_nodes):
        if node.left is not None:
            self.__nodes_list(node.left, sorted_nodes)

        sorted_nodes.append((node.key, node.value))

        if node.right is not None:
            self.__nodes_list(node.right, sorted_nodes)

    def height(self) -> int:
        return self._root.height() if not self.is_empty() else 0


def main():
    tree = BSTTree()
    keyvalue = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 20: 'E', 58: 'F', 91: 'G', 3: 'H', 8: 'I', 37: 'J', 60: 'K', 24: 'L'}
    for key in keyvalue:
        tree.insert(key, keyvalue[key])
    tree.print_tree()
    print(tree)
    print(tree.search(24))
    tree.insert(20, "AA")
    tree.insert(6, "M")
    tree.delete(62)
    tree.insert(59, "N")
    tree.insert(100, "P")
    tree.delete(8)
    tree.delete(15)
    tree.insert(55, "r")
    tree.delete(50)
    tree.delete(5)
    tree.delete(24)
    print(tree.height())
    print(tree)
    tree.print_tree()


if __name__ == "__main__":
    main()
