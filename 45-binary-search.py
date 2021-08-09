# why wont we do 
# lo=cur and hi=cur
#
# because if cur==lo==hi-1 and k>A[cur]
# lo=cur; cur=int((2*hi-1)/2) == hi-1;
# so, still cur==lo==hi-1 and k>A[cur]
# loop is infinite (always lo<=hi)
# Note. we have these indices eventually if k>A[hi-1]
#
# other way around
# if cur==lo==hi-1 and k<A[cur]
# hi = cur;
# so cur==lo==hi
# loop is infinite (always lo<=hi)
# Note. we have these indices eventually if k<A[lo]
#
# if A[cur] != k it is completely safe to 
# move hi/lo to left/right of cur, respectively

def binary_search(A=[0,1,2,3,4], k=0):
    
    lo = 0
    hi = len(A)-1

    while lo <=hi:
        cur = int((hi+lo)/2)

        print(lo, cur, hi)

        if A[cur]==k:
            return cur
        elif A[cur]<k:
            lo=cur+1
            
        else:
            hi=cur-1
            
binary_search([0,1,2,3,4], 3.1)