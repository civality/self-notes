# keep indices for each list 
# in each iteration determine minimum array element
# at those indices
# cur determines which list has minimum value currently
#
# lists[cur]   
# indices[cur] 
# are focused list and index respectively
# 
# (2) if a list is fully traversed make its index None
# (1) same as merged.append(lists[cur][indices[cur]])


def merge(lists):
    
    indices = [0]*len(lists)
    merged = []

    total = sum([len(l) for l in lists])
    z=0

    while z<total:

        mymin = None
        cur = 0

        for i,j in enumerate(indices):
            if j is not None:
                if mymin is None or lists[i][j] < mymin:
                    mymin=lists[i][j]
                    cur=i
                    

        merged.append(mymin) # (1)

        #print('indices', indices)
        #print(merged)
        z += 1

        indices[cur] += 1
        if indices[cur] >= len(lists[cur]): # previous bug due to len(lists)
            indices[cur] = None # (2)

    return merged

lists = [
  [2.5, 7.5],  
  [-1,1,3,5,6],  
  [2,4,7],
  [0,7,9]
]
merge(lists)