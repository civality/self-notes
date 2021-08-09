Question:

[4,0,1,6,7,9,3]

from abobe, build below

    6
  0   9
4  1  7  3


Solution

remember indices of heap

   0
 1   2
3 4  5 6

l = p*2 +1
r = p*2 +2 
p = floor(((l or r)-1) /2)


# [0,1,2]3[4,5,6]
# [0]1[2]
#  0     
#  2
# [4]5[6]
#  4
#  6
# 
# in lo==hi==cur  calls i.e 0 2 4 6
# if we had this: <if lo>=hi: return> we would not add 0 2 4 6 to tree
#
#  Very sneaky bug: if not hi: block is intented hi=len(A)-1 as default argument if hi is none
#                   but expression is also True when hi==0
#                   so whenever we get to hi==0 it again makes it len(A)-1, recursion never stops
#                   so make it xplicit  if hi is None:

def add_tree(A=[0,1,2,3,4,5,6], lo=0, hi=None):
    
    if hi is None: 
        hi=len(A)-1
        
    if lo>hi:
        return

    cur = int((lo+hi)/2) #dont forget lo+hi parenthesis
    
    #tree.insert(A[cur])
    print(A[cur])
    add_tree(A, lo, cur-1)
    add_tree(A, cur+1, hi)

add_tree([0,1,2,3,4,5,6], 0, 6)


    
# https://stackoverflow.com/questions/16317537/creating-an-unsorted-binary-tree-from-an-array-which-will-be-like-a-heap-ie-sto