from BST_tree import *


class AVLNode(Node):
    def __init__(self, key: int, value, right=None, left=None):
        super().__init__(key, value, right, left)
        self.node_height = 1

    def insert(self, key, value):
        if key == self.key:
            self.value = value

        elif key < self.key:
            if self.left is not None:
                self.left.insert(key, value)
            else:
                self.left = AVLNode(key, value)

        else:
            if self.right is not None:
                self.right.insert(key, value)
            else:
                self.right = AVLNode(key, value)

    def balance_factor(self) -> int:
        left_height = self.left.node_height if self.left is not None else 0
        right_height = self.right.node_height if self.right is not None else 0
        return left_height - right_height

    def new_height(self):
        left_height = self.left.node_height if self.left is not None else 0
        right_height = self.right.node_height if self.right is not None else 0
        self.node_height = max(left_height, right_height) + 1


class AVLTree(BSTTree):
    def __init__(self):
        super().__init__()

    @staticmethod
    def left_rotation(node: AVLNode) -> AVLNode:
        new_root = node.right
        n0 = new_root.left
        new_root.left = node
        node.right = n0

        return new_root

    @staticmethod
    def right_rotation(node: AVLNode) -> AVLNode:
        new_root = node.left
        n0 = new_root.right
        new_root.right = node
        node.left = n0

        return new_root

    def balance(self, node: AVLNode, parent: Optional[AVLNode], which_child: Optional[str]):
        if node is None:
            return None

        self.balance(node.right, node, "right")
        self.balance(node.left, node, "left")

        bal = node.balance_factor()

        if bal < -1:  # Wymagana rotacja w lewo
            bal_r_child = node.right.balance_factor() if node.right is not None else 0
            if bal_r_child > 0:
                node.right = AVLTree.right_rotation(node.right)

            if parent is not None:
                if which_child == "left":
                    parent.left = AVLTree.left_rotation(node)
                elif which_child == "right":
                    parent.right = AVLTree.left_rotation(node)
                else:
                    raise ValueError("Invalid arg: which_child!")
            else:
                self._root = AVLTree.left_rotation(node)

            return

        if bal > 1:  # Wymagana rotacja w prawo
            bal_l_child = node.left.balance_factor() if node.left is not None else 0
            if bal_l_child < 0:
                node.left = AVLTree.left_rotation(node.left)

            if parent is not None:
                if which_child == "left":
                    parent.left = AVLTree.right_rotation(node)
                elif which_child == "right":
                    parent.right = AVLTree.right_rotation(node)
                else:
                    raise ValueError("Invalid arg: which_child!")
            else:
                self._root = AVLTree.right_rotation(node)

            return

        node.new_height()

    def insert(self, key: int, value):
        if self.is_empty():
            self._root = AVLNode(key, value)
        else:
            self._root.insert(key, value)

        self.balance(self._root, None, None)

    def delete(self, key: int):
        super().delete(key)

        self.balance(self._root, None, None)


def main():
    tree = AVLTree()
    key_value = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 2: 'E',
                 1: 'F', 11: 'G', 100: 'H', 7: 'I', 6: 'J',
                 55: 'K', 52: 'L', 51: 'M', 57: 'N', 8: 'O',
                 9: 'P', 10: 'R', 99: 'S', 12: 'T'}
    for key in key_value:
        tree.insert(key, key_value[key])
    tree.print_tree()
    print(tree)
    print(tree.search(10))
    tree.delete(50)
    tree.delete(52)
    tree.delete(11)
    tree.print_tree()
    tree.delete(57)
    tree.delete(1)
    tree.delete(12)
    tree.insert(3, 'AA')
    tree.insert(4, 'BB')
    tree.delete(7)
    tree.delete(8)
    tree.print_tree()
    print(tree)


if __name__ == "__main__":
    main()
