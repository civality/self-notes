# Sometimes you set up base cases such that
# - root is None  
# - root is leaf  or
#  
# 
# we use validate-bst to illustrate this

global prev
prev = float('-inf')


#Runtime: 40 ms, faster than 86.50% of Python3 online submissions for Validate Binary Search Tree.
#Memory Usage: 16.9 MB, less than 27.04% of Python3 online submissions for Validate Binary Search Tree.
def helper(root:TreeNode):

    if not root:
        return True
    
    if not helper(root.left):
        return False
    
    if root.val <= prev:
        return False
    
    prev = root.val
    
    return helper(root.right)
    

# Runtime: 40 ms, faster than 86.50% of Python3 online submissions for Validate Binary Search Tree.
# Memory Usage: 16.8 MB, less than 29.09% of Python3 online submissions for Validate Binary Search Tree.
def helper(root:TreeNode):

    if root.left and not helper(root.left):
        return False
    
    if root.val <= prev:
        return False
    
    prev = root.val
    
    if root.right:
        return helper(root.right)
    
    return True



# Extra care:
# -2**31 <= Node.val <= 2**31 - 1
# So if you initiate self.prev = -2**31
# you face error when input is [-2**31]
# you should initiate self.prev = (-2**31)-1 or float('-inf')
