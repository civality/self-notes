class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
            
class Solution:
    
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        
        diameter = [0]
        self.helper(root, diameter)
        
        return diameter[0]
        

    # dont forget self. prefix
    # dont forget diameter argument
    def helper(self, root:TreeNode, diameter):
        
        if root == None:
            return 0
        
        lmax = self.helper(root.left, diameter)
        rmax = self.helper(root.right, diameter)
        
        if diameter[0] < lmax + rmax:
            diameter[0] = lmax + rmax
            
        return 1 + max(lmax, rmax)
    
    
    def array_to_tree(self, A):

        nodes = [TreeNode(val) for val in A]
        for i in range(len(A)-1, 0, -1):
            p = (i-1)/2

            if p == int(p): #i is left child
                nodes[int(p)].left=nodes[i]
            else:
                nodes[int(p)].right=nodes[i]

            nodes.pop()

        root = nodes[0]
        return root
    
sol = Solution()
# Todo, fix none case. It creates a TreeNode with val=None
# We dont want a TreeNode, we want None!
# root = sol.array_to_tree(A=[1,2,None,4,5,6,7,8])
# edit: leetcode doesnt accept A with None either, anyways.

root = sol.array_to_tree([1,2])
print(sol.diameterOfBinaryTree(root)) # 1

root = sol.array_to_tree([1,2,3,4,5])
print(sol.diameterOfBinaryTree(root)) # 3 

root = sol.array_to_tree([1,2,3,4,5,6,7,8])
print(sol.diameterOfBinaryTree(root)) # 5


#https://leetcode.com/problems/diameter-of-binary-tree/