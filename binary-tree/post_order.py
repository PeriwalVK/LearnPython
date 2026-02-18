# Python program to print Post-Order traversal
# using stack.
from typing import List


class Node:
    def __init__(self, x):
        self.data = x
        self.left: Node = None
        self.right: Node = None

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)


def PostOrder_recursive(root: Node):

    arr = []

    def _postorder(node: Node):
        if node:
            _postorder(node.left)
            _postorder(node.right)
            arr.append(node.data)

    _postorder(root)
    return arr


def PostOrder_2_stacks(root: Node):
    """
    Logic very similar to Reverse Modified Preorder (Elegant Trick)

        Preorder = Root → Left → Right

        If we change to: Root → Right → Left (thats why we are pushing left first in stack_node)
        and reverse it → we get Postorder. (collecting from stack_visited is basicaly reversing it)

    """

    if not root:
        return []

    ans = []
    stack_node: List[Node] = []
    stack_visited: List[Node] = []
    stack_node.append(root)

    while stack_node:
        curr_node = stack_node.pop()
        stack_visited.append(curr_node.data)

        # push left, then right
        # so that right comes out before left and goes first into stack_visited
        # and in the end left comes out before right while popping from stack_visited
        if curr_node.left:
            stack_node.append(curr_node.left)
        if curr_node.right:
            stack_node.append(curr_node.right)

    while stack_visited:
        ans.append(stack_visited.pop())

    return ans


def PostOrder_single_stack(root: Node):
    ans = []
    stack: List[Node] = []

    last_visited: Node = None
    curr_node = root

    while stack or curr_node:
        # Reach the left most Node of the curr Node
        # keep pushing all the nodes in the path
        while curr_node:
            stack.append(curr_node)
            curr_node = curr_node.left

        # encountered left child as None, hence pick-last left
        curr_node = stack[-1]  # root

        # check if its right has been just visited or not
        # if not then just repeat the process for right subtree
        # else since left is done and right is last visited, its time to process self
        if curr_node.right and last_visited is not curr_node.right:
            curr_node = curr_node.right
            continue
        else:
            last_visited = curr_node
            ans.append(curr_node.data)
            stack.pop()
            curr_node = None

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

    print(f"POSTORDER RECURSIVE:\t\t{PostOrder_recursive(root)}")
    print(f"POSTORDER 2 STACKS:\t\t{PostOrder_2_stacks(root)}")
    print(f"POSTORDER SINGLE STACKS:\t{PostOrder_single_stack(root)}")
