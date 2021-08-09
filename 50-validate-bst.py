# Assume cur must be strictly greater or lesser

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
def array_to_tree(A):

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


def isValidBST(root: TreeNode) -> bool:
    curmin, curmax, curvalid = helper(root)
    return curvalid

# Wrong version because
# imagine very basic tree with only node root = 1
# since it is on leaf, it makes a final call and gets
# (-2**31, True) = (lmax, lvalid)
# (-2**31, True) = (rmax, rvalid)
# root.val>lmax  this one is OK but
# root.val<rmax  this one is always false

def helper_old(self, root:TreeNode):
    
    if root is None:
        return (-2**31, True)
    
    lmax, lvalid = self.helper_old(root.left)
    rmax, rvalid = self.helper_old(root.right)
    
    curmax = max(lmax, rmax, root.val) # careful not self.val
    curvalid = root.val>lmax and root.val<rmax and lvalid and rvalid
    
    return (curmax, curvalid)

# lmax>root.val => curvalid=False is OK
# rmax>root.val => curvalid=False is WRONG
# rmax<root.val => curvalid=False would be even WRONG because you would miss 1 below:
#       2
#         3 
#       1   4
#
# rmin<root.val => curvalid=False should be CORRECT check

def helper_old2(self, root:TreeNode):
    
    if root is None:
        return (None, True)
    
    lmax, lvalid = self.helper_old2(root.left)
    rmax, rvalid = self.helper_old2(root.right)
    
    curmax = root.val
    curvalid = True
    
    if lmax is not None:
        
        if lmax>curmax:
            curmax=lmax
        
        if lmax>root.val:
            curvalid=False
        
    if rmax is not None:
        
        if rmax>curmax:
            curmax=rmax
        
        if rmax<root.val:
            curvalid=False
        
    return (curmax, curvalid)


# If any of the subtrees is invalid, we must immediately return valid=False
# otherwise this tree would return true:
#
#       10 
#    5      15
#  2   4  14 
# 
# Also, this is early stoopping and good for performance
# careful, in early stopping if we cant just return False
# return value must be 3-tuple
# careful! if we return (None, None, False) the "if" conditions 
# are skipped and we return (curmin, curmax, True) at the bottom
#       right? no. thankfully we have if not (lvalid and rvalid)
#
# Also, dont do (if lmax>root.val) (if rmin<root.val) use >= <= respectively
#
# Runtime: 48 ms, faster than 33.85% of Python3 online submissions for Validate Binary Search Tree.
# Memory Usage: 16.9 MB, less than 22.82% of Python3 online submissions for Validate Binary Search Tree.
#
# this version works but needs optimization: if lvalid==False, why do you calculate rvalid?
# By the way we cannot just check violations for direct childs root.val>root.left.val 
# becaususe it would be wrong in this case:
#       10 
#    5      15
#  2   11  14 

def helper_old3(root:TreeNode):
    
    if root is None:
        return (None, None, True)
    
    lmin, lmax, lvalid = helper_old3(root.left)  
    rmin, rmax, rvalid = helper_old3(root.right) 

    if not (lvalid and rvalid): 
        return (None, None, False)

    curmin = root.val
    curmax = root.val
    #curvalid = True #commented out for early stopping

    if lmax is not None: #it means lmin is not None
        #print(f'root.val {root.val}', f'lmax {lmax}') #good debug checkpoint
        if lmax>=root.val:
            #curvalid=False #commented out for early stopping
            return (None, None, False) 

        if lmax>curmax:
            curmax=lmax

        if lmin<curmin:
            curmin=lmin

    if rmax is not None: #it means rmin is not None
        #print(f'root.val {root.val}', f'rmax {rmax}') #good debug checkpoint

        if rmin<=root.val:
            #curvalid=False #commented out for early stopping
            return (None, None, False)

        if rmax>curmax:
            curmax=rmax

        if rmin<curmin:
            curmin=rmin
    
    #print(f'root.val {root.val}', f'curvalid {curvalid}') #good debug checkpoint
    
    #return (curmin, curmax, curvalid) #commented out for early stopping
    return (curmin, curmax, True)



# Runtime: 48 ms, faster than 33.85% of Python3 online submissions for Validate Binary Search Tree.
# Memory Usage: 16.8 MB, less than 29.09% of Python3 online submissions for Validate Binary Search Tree.
#
# Further Optimization needed:
# you don't really need lmin when checking validity of left subtree
# you don't really need rmax when checking validity of right subtree
# but you need them both, because you dont known whether they will be used
# lmax>=root.val or rmin<=root.val in the next execution
# in this solution
# you are not exactly doing pre/in/post order traversal
# you are doing left, (cur vs lmax), right, (cur vs rmin)
# 
def helper_old4(root:TreeNode):
    
    lmin=root.val; rmax=root.val

    if root.left is not None:
        lmin, lmax, lvalid = helper_old4(root.left)
        
        if not lvalid or lmax>=root.val:
            return (None, None, False)

    if root.right is not None:
        rmin, rmax, rvalid = helper_old4(root.right)
        if not rvalid or rmin<=root.val:
            return (None, None, False)
    
    return (lmin, rmax, True)


# Runtime: 40 ms, faster than 86.50% of Python3 online submissions for Validate Binary Search Tree.
# Memory Usage: 16.8 MB, less than 29.09% of Python3 online submissions for Validate Binary Search Tree.
# power of inorder traversal
def isValidBST(self, root: TreeNode) -> bool:
        self.prev = float('-inf')
        return self.helper(root)
        
    
    def helper(self, root:TreeNode):

        if root.left and not self.helper(root.left):
            return False
        
        if root.val <= self.prev:
            return False
        
        self.prev = root.val
        
        if root.right:
            return self.helper(root.right)
        
        return True



# [1,1]
#   1
# 1

root = array_to_tree([1,1])
print(helper(root)) # False


# [1,2]
#
#       1 
#    2   

root = array_to_tree([1,2])
print(helper(root)) # False


# [10,5,15,2,4,14]
#
#       10 
#    5      15
#  2   4  14 

root = array_to_tree([10,5,15,2,4,14])
print(helper(root)) #False


# [10,5,15,2,11,14]
#
#       10 
#    5      15
#  2   11  14 

root = array_to_tree([10,5,15,2,11,14])
print(helper(root)) #False


# [10,5,15,2,11,14]
#
#       10 
#    5      15
#  2   6  14 

root = array_to_tree([10,5,15,2,6,14])
print(helper(root)) #True

# [1]
root = array_to_tree([1])
print(helper(root)) #True



# https://leetcode.com/problems/validate-binary-search-tree/