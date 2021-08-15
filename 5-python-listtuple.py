<------------------------
data = [1,2,3,4,5,6]
data[0::2] # [1, 3, 5] (index % 2 == 0)  
data[0::3] # [1, 4]    (index % 3 == 0)
data[1::2] # [2, 4, 6] (index % 2 == 1)
------------------------>

<------------------------
len, abs, zip, ... are called built-in functions
------------------------>

<------------------------
#very important bug preventer

L1 = [{'a':1}]
L2 = L1.copy()
L1[0]['a']=5
print(L1) # [{'a': 5}]
print(L2) # [{'a': 5}]


# If the list contains objects and you want 
# to copy them as well, use generic copy.deepcopy():

import copy

L1 = [{'a':1}]
L2 = copy.deepcopy(L1)
L1[0]['a']=5
print(L1) # [{'a': 5}]
print(L2) # [{'a': 1}]
------------------------>

<------------------------
#Extra info: max(1,2,None) #TypeError: '>' not supported between instances of 'NoneType' and 'int'
------------------------>

<------------------------
A = [15,2,7,0,1,8,9,13,1]

def trysort(A):
    sorted(A) #Not inplace, return a new list
    
print(A)
trysort(A)
print(A) #doesnt change
------------------------>

<------------------------
Empty list

The pythonic way to do it is from the PEP 8 style guide 
(where Yes means “recommended” and No means “not recommended”):

For sequences, (strings, lists, tuples), use the fact that empty sequences are false.

Yes: if not seq:
     if seq:

No:  if len(seq):
     if not len(seq):
------------------------>

<------------------------
def divide(a,b):
    try:
        c = a/b
        return c
    except Exception as e:
        pass

print(divide(3,5)) # 0.6
print(divide(3,0)) # None
------------------------>

<------------------------
l = ['a','b','c']
d = dict.fromkeys(l, [0,0])

print(d) # {'a': [0, 0], 'b': [0, 0], 'c': [0, 0]}
 
d['a'] is d['b'] # True, This is dangerous

# Trick here is 

value = [0, 0]
print(id(list(value))) #..60424
print(id(list(value))) #..58632

# so 
l = ['a','b','c']
value = [0, 0]
d = {key: list(value) for key in l}
 
print(d) # {'a': [0, 0], 'b': [0, 0], 'c': [0, 0]}
d['a'] is d['b'] # False, This is safe


https://stackoverflow.com/questions/15516413/dict-fromkeys-all-point-to-same-list
------------------------>

<------------------------
type({}) # dict
type({1}) # set
type({1,2}) # set
------------------------>

<------------------------
# when dict changes, dictionary.keys(), dictionary.items() also changes dynamically

A = {'a':0,'b':1}
b = A.keys() # dict_keys(['a', 'b'])
c = A.values() # dict_values([0, 1])
A['a']=10
print(c) # dict_values([10, 1])

https://codeburst.io/dictionary-view-objects-101-480b72f71dec
------------------------>

<------------------------
l = [x for x in range(100)]

#1
looking_for = 98   
for i, el in enumerate(l)
    if el == looking_for:
        return True 

#2
looking_for in l  

2 does actually 1 so, it is O(N)
------------------------>

<------------------------
#Edit: this example needs editing later
import numpy as np
import numpy.ma as ma


C =[[ 6,  7,  8],
    [15, 80, 78]]

mask = np.full((len(supply), len(demand)), False)
Cm = ma.masked_array(C, mask)
mask2 = np.full((len(supply), len(demand)), False)
Cm2 = ma.masked_array(Cm, mask2)

print(Cm)
print(mask)
print(Cm2)
print(mask2)

mask[:,2]=True

print(Cm)
print(mask)
print(Cm2)
print(mask2)

mask2[0]=True

print(Cm)
print(mask)
print(Cm2)
print(mask2)
------------------------>

<------------------------
a = np.array([90,10,30,40,80,70,20,50,60,0])
print(np.partition(a, 4)) # sadece 5. element yeri kesin
print(np.argpartition(a, 4)) # sadece 5. element indexi kesin
------------------------>

<------------------------
a = 3
b = 4
a, b = b, a

print(a,b) # 4 3


A = [1, 2, 3, 4]
A[0], A[2] = A[2], A[0]
print(A) # [3 2 1 4]
------------------------>

<------------------------
A = ([1, 2, 3, 4, 5, 6])
A # [1, 2, 3, 4, 5, 6]

A = (
    [1,2] +
    [3,4] +
    [5,6]
)

print(A) # type list

A = (
    [1,2] +
    [3,4] +
    [5,6],
)

print(A) # type tuple
------------------------>

# Note in python if we say 
# x = a,b 
# y = (a,b)
# both x and y are tuple and x == y is true 
# 
# list( (1, 2, 3) ) is [1, 2, 3]
# [ (1, 2, 3) ]     is [ (1, 2, 3) ] 

# x = ( 2 * o for o in [1,2,3] )  is generator object
# y = [ 2 * o for o in [1,2,3] ]  is list
# [ 2 * o for o in x ]  is  [4, 8 , 12] # 1 st run
# [ 2 * o for o in x ]  is  []         # 2 nd run, because generator completes
# 
# [ 2 * o for o in y ]  is  [4, 8, 12] # in all runs

# type(int) type
# type(list) type
# type(type) type
# isinstance(int, type) =True

# id(4)   
# x = [1, 2, 3]
# id(x)  
# id(int) 
# id(type)
# all above results in a 10-digit integer

# id('A')
# id('A')
# two ids above are same

# id( [1, 2, 3])
# id( [1, 2, 3])
# two ids above are different

# def double(z):
#    return z * 2
# x = [1, 2, 3]
# tuple(map(double, x))  =(2, 4, 6)

# print((2,3) == (2,3))
# print((2,3) is (2,3))
# print([2,3] == [2,3])
# print([2,3] is [2,3]) # only this False

