# I implemented all by myself, before looking at any solution
# also my solution is more general as the link is about only binary tree
# https://www.geeksforgeeks.org/print-k-sum-paths-binary-tree/


# elements can be negative
# path can start from any node end at any node
# path direction must be downward
# print all paths that is equal to k

class Node:
    
    def __init__(self, val):
        self.val = val
        self.children = None
        self.delay = None

    def add_child(self, child):
        if self.children:
            self.children.append(child)
        else:
            self.children = [child]
        
    def add_children(self, list_values):
        self.children = [Tree(val) for val in list_values]
    
    def write(self):
        
        if self.delay:
            print(f'({self.delay})', end='')
            
        print(self.val)
        
        if self.children:
            for child in self.children:
                child.write()
    
    def get_max_path(self):
        
        total = self.val
        if self.children:
            the_list = []
            for child in self.children:
                the_list.append(child.get_max_path())
            total += max(the_list)
    
        return total
    
    # for each node, you need to iterate all subtree (postfix iterations), so it seems exponential
    # method returns list of lists
    # each list is postfix from current node (including current node)
    # 
    # method does this:
    # for each postfix (including current node), check its all prefixes
    # if sum(prefix) == k, print it
    # bug: if some prefixes of different posftixes are the same
    # as in below [1,2,8] [1,2,9] when cur is root.
    # if k=5 we will print 2,1,2 twice, for same path
    """
         2
        / \
       /   \
      5     1
     (7)   /|\
          / | \
         2  1  2
        /\
       9  8 
     """
    # we still cannot discard one prefix because what if they continue like that?
    # [1,2,8,-8] [1,2,9,-9] they are two distinct paths now.
    # that leads us to other implementation 
    
    def k_sum_path_old(self, k):
        
        # careful this should be at the very beginning
        if self.val == k: 
            print(self.val)
            
        if self.children:
            the_list = []
            for child in self.children:
                the_list += child.k_sum_path_old(k)
            
            for postfix in the_list:
                
                total = self.val #careful, this should be inside for loop
                print(postfix)
                for i, elm in enumerate(postfix):
                    total += elm
                    if total == k:
                        print(self.val,'@',postfix)
                        print(self.val, *postfix[:i+1])
                        
                
            the_list_2 = []
            for e in the_list:
                the_list_2.append([self.val] + e)
            return the_list_2
                
        else:
            return [[self.val]]


    # go from top down, carry prefix as list to child
    # carry prefix sum to child to avoid prefix iteration
    # carry k 
    # if prefix sum + cur.val == k: print prefix
    # careful, prefix should be deep clone, otherwise a sibling runis prefix
    # it solved previous issue but now only paths from root is printed
    # what if k=3 in this subtree
    '''
         2
        / \
       /   \
      5     1
     (7)   /|\
          / | \
         2  1  2
        /\
       9  8 
    '''
    # only [2,1] is printed
    # also to make deep clone, it is inevitable to iterate each prefix
    # carrying prefix_sum can't save us for list iteration
    # besides, even only printing a prefix is O(len(prefix)), 
    # so no parsimony is meaningful
    # that leads us to other implementation 
    def k_sum_path_old2(self, k, prefix=[], prefix_sum=0):
        
        if self.val == k:
            print(self.val)
        
        if prefix_sum + self.val == k:
            print(*prefix, self.val)
            
        if self.children:
            prefix = prefix.copy()
            prefix.append(self.val)
            for child in self.children:
                child.k_sum_path_old2(k, prefix=prefix, prefix_sum=prefix_sum+self.val)
    

    # no need to carry prefix sum; can't avoid prefix iteration
    # append cur.val to prefix
    # iterate each postfix of the prefix (backwards)
    # 
    # this way we guarantee that we iterate
    # each postfix that ends with cur.val only once
    # careful, prefix should be deep clone, otherwise a sibling runis prefix

    def k_sum_path(self, k, prefix=[]):
        
        prefix = prefix.copy()
        prefix.append(self.val)
        
        for i in range(1, len(prefix)+1):
            postfix = prefix[-i:]
            if sum(postfix) == k:
                print(*postfix)
        
        if self.children:
            for child in self.children:
                child.k_sum_path(k, prefix=prefix)


'''
     2
    / \
   /   \
  5     1
 (7)   /|\
      / | \
     2  1  2
    /\
   9  8 
'''

root = Node(2)
cur = Node(5)
root.add_child(cur)

cur = Node(1)
cur2 = Node(2)
cur2.add_child(Node(9))
cur2.add_child(Node(8))
cur.add_child(cur2)
cur.add_child(Node(1))
cur.add_child(Node(2))
root.add_child(cur)

cur = Node(30)
root.add_child(cur)

root.write()
print()
root.k_sum_path_old(2)
print()
root.k_sum_path_old(5)

print()
root.k_sum_path_old2(2)
print()
root.k_sum_path_old2(5)
print()
root.k_sum_path_old2(3)

print()
root.k_sum_path(2)
print()
root.k_sum_path(5)
print()
root.k_sum_path(3)
print()
root.k_sum_path(14)
