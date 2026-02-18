# Python program to print Pre-Order traversal
# using stack.
from typing import List


class Node:
    def __init__(self, x):
        self.val = x
        self.left: Node = None
        self.right: Node = None

    def __str__(self):
        return str(self.val)


def PreOrder_recursive(root: Node):

    arr = []

    def _preorder(node: Node):
        if node:
            arr.append(node.val)
            _preorder(node.left)
            _preorder(node.right)

    _preorder(root)
    return arr


def PreOrder_without_recursion(root: Node):
    ans = []
    stack: List[Node] = []
    stack.append(root)

    while stack:
        # process self first
        curr = stack.pop()
        ans.append(curr.val)

        # push right first, then left,
        # so that left comes out before right
        if curr.right:
            stack.append(curr.right)
        if curr.left:
            stack.append(curr.left)

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

    print(f"PREORDER RECURSIVE:\t{PreOrder_recursive(root)}")
    print(f"PREORDER NON RECURSIVE:\t{PreOrder_without_recursion(root)}")
