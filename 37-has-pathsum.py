# don't forget to add self in each member function
# Note: never forget "self" for method definiton, and method calls within object
# def method(self, ...)    
# self.method(...) #no self as argument
# child.method(...) # or careful if you want to call child


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
    

    '''
         2
        / \
       /   \
      5     1
     (7)   /|\
          / | \
         2  1  2
        (5)(4)(5)
    '''

    # Given this
    # Each node represents an execution time.
    # we want to add delays to some nodes so that
    # all paths from root to leaves must be equal
    # try to add minimum number of delays
    # try to keep total delay minimum

    # Solution is O(n) because a subtree is called only once
    # we do one traversal to find (outside of this method) global_max_path
    # total number branchings is O(n)
    # don't worry about lists iterations in this method.
    # if a node has k children, k branching will be done; iterated lists are length of k; 
    # and there is a constant amount of list iterations (3 to be precise)
    # Other thing, we need aggregation of values returned by all children (min for example)
    # a node has to wait for results from all its siblings
    # therefore, a node's value can only be modified by its parent (not by itself)

    def add_delay(self, pathlen):

        # pathlen here is global_max_path - sum(prefix path) 
        # prefix path sum excludes root value of this subtree
        # pathlen is just a tool to determine required delays for each path in entire tree
        # we could've used two parameters to be more clear
        # like this: add_delay(self, global_max_path, prefix_path) 

        if self.children:
            the_list = []
            for child in self.children:
                the_list.append(child.add_delay(pathlen - self.val))
            
            # childs return value is delay to distribute to prefix path (including child)
            # we will distribute delay i  to [root ... current, child_i] for each i
            # our goal is to distribute delay to [root ... current] as much as possible
            # but this delay can be maximum min(the_list)
            # add excess delays to child nodes
            # if our goal was to distribute delay to [root ... current] as small as possible
            # just add delays to child.vals and distribute 0 above

            # at this point, all paths of a child subtree = child.get_max_path()
            # but this number is different for each child
            # to make all equal, increment child.val 

            required_delay = min(the_list)
            the_list = [e - required_delay for e in the_list]
            for i, child in enumerate(self.children):
                #child.val += the_list[i] # if you dont want to use separate delay variable
                child.delay = the_list[i] # creates a new variable
            
            # at this point, all paths to leaf from root of this subtree is equal
            # and this is equal to max_path of original subtree

            # required_delay here is pathlen - max_path of original subtree
            # required delay is delay to distribute to prefix path (including this node)
            # this node will get its share by its parent
            return required_delay
        
        else:
            return pathlen - self.val


    # finds a root to leaf path sum
    # in freecodecamp recursion problems
    # generally base case when number hits 0
    # but here, with a prebuilt tree, you can only traverse 
    # until you hit a leaf node
    # base case num == self.val pattern is reasonable therefore
    def hasPathSum(self, num):
        
        if self.children:
            ans = False
            the_list = []
            # you can do early stopping here (short circuit)
            for child in self.children:
                the_list.append(child.hasPathSum(num-self.val))
            return any(the_list)
            
        else:
            return num==self.val


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
print(root.hasPathSum(4)) # True
print(root.hasPathSum(32)) # True
print(root.hasPathSum(0)) # False
print(root.hasPathSum(15)) # False



# To solve add delay, we can construct a binary tree from scracth,
# after traversing and getting delay values for each child of root
# but wait .. no can't do it easily