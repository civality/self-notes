for i in range(0,4):
    for j in range(0,4):
        if i==1 and j==1: 
            break
        print(i,j)

"""
0 0
0 1
0 2
0 3
1 0
2 0
2 1
2 2
2 3
3 0
3 1
3 2
3 3


it doesnt only break j loop, also breaks i loop and i skips to 2 and  j gets back to 0 
"""
