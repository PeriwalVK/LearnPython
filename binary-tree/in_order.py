# Python program to print In-Order traversal
# using stack.
from typing import List


class Node:
    def __init__(self, x):
        self.val = x
        self.left: Node = None
        self.right: Node = None

    def __str__(self):
        return str(self.val)


def inorder_recursive(root: Node):

    arr = []

    def _inorder(node: Node):
        if node:
            _inorder(node.left)
            arr.append(node.val)
            _inorder(node.right)

    _inorder(root)
    return arr


def inOrder_without_recursion(root: Node):
    ans = []
    stack: List[Node] = []
    curr = root

    while curr or stack:
        # Reach the left most Node of the curr Node
        # keep pushing all the nodes in the path
        while curr:
            stack.append(curr)
            curr = curr.left

        # encountered left child as None, hence pick self and process
        curr = stack.pop()
        ans.append(curr.val)

        # we have visited the self, so now process right subtree similarly
        curr = curr.right

    return ans


if __name__ == "__main__":
    # Constructed binary tree is
    #          1
    #        /   \
    #      2      3
    #    /  \    /  \
    #  4     5  6    7
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)

    print(f"INORDER RECURSIVE:\t{inorder_recursive(root)}")
    print(f"INORDER NON RECURSIVE:\t{inOrder_without_recursion(root)}")
