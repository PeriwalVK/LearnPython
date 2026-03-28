class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def morris_inorder_original(root):
    """
    Morris Inorder Traversal
    Time: O(n)
    Space: O(1)
    """
    result = []
    current = root

    while current:
        # if I don't have a left child => then visit me and move to my right
        if not current.left:
            print(f"VISITED {current.val} (No left child)")
            result.append(current.val)
            
            current = current.right # them move to right
        
        # else (my left child exists) 
        else:
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                # will break if 
                #   predecessor has no right child, 
                #   or predecessor has a backlink to current 
                predecessor = predecessor.right
            
            # First Calculated my predecessor

            # IF no right child of predecessor -> means backlink not yet created -> create it 
            if not predecessor.right:
                print(f"Created backlink: {predecessor.val} -> {current.val}")
                predecessor.right = current # created backlink
                
                current = current.left # now I can move to my left without any worry of how I'll come back

            # Else predecessor.right == current
            # means backlink exists → means I have already visited my left child earlier 
            # (tabhi to I already have a back link) 
            # -> so now remove it and visit me and then move to my right now
            else:
                print(f"Removed backlink: {predecessor.val} -> {current.val}")
                predecessor.right = None
                
                print(f"VISITED {current.val} (left subtree fully visited, came back via backlink)")
                result.append(current.val)
                
                current = current.right
        


    return result



def morris_inorder(root):
    """
    Morris Inorder Traversal
    Time: O(n)
    Space: O(1)
    """
    result = []
    curr = root

    while curr:
        if curr.left:
            pred = curr.left
            while pred.right and pred.right != curr:
                pred = pred.right
            
            if not pred.right:
                pred.right = curr
                curr = curr.left
            else: # pred.right == curr
                pred.right = None
                result.append(curr.val)
                curr = curr.right
        else:
            result.append(curr.val)
            curr = curr.right
    
    return result



# -------------------------------
# 🔨 Build Example Tree
# -------------------------------
def build_tree():
    """
        4
       / \
      2   6
     / \ / \
    1  3 5  7
    """
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(6)

    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)

    root.right.left = TreeNode(5)
    root.right.right = TreeNode(7)

    return root


# -------------------------------
# 🚀 Run Example
# -------------------------------
if __name__ == "__main__":
    root = build_tree()

    print("Morris Inorder Traversal Steps:\n")
    result = morris_inorder(root)

    print("\nFinal Inorder Traversal:")
    print(result)
