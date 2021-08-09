def staircase(N=5, step=[1,2,3]):
    
    if N==0:
        return 1
    if N<0:
        return 0
    
    total = 0
    
    for s in step:
        if s: # to skip s in {0,None}
            total += staircase(N-s, step) #dont forget to pass step
    
    return total
    #dont forget to return
    
staircase(50, [2,3]) #gets slower
staircase(60, [2,3]) #gets even slower


# Memoized version
def staircase(N=5, step=[1,2,3], memo={}):
    if N in memo:
        return memo[N]
    if N==0:
        return 1
    if N<0:
        return 0
    
    total = 0
    
    for s in step:
        if s: # to skip s in {0,None}
            total += staircase(N-s, step) #dont forget to pass step
    
    memo[N] = total
    return total
    #dont forget to return
    
staircase(50, [2,3]) #very fast
staircase(60, [2,3]) #very fast
staircase(300, [2,3]) #very fast


# Tabulated solution for simpler problem assume always steps=[1,2]
# problem is same as fibonacci
# A = [1,1] # 0, 1 base cases
# len(A) will eventually be A+1
# remember, in tabulation usually N+1 array is allocated

def staircase(N=5):
    if N == 0 or N==1:
        return 1
    
    A = [1,1]
    
    for i in range(N-1):
        A.append(A[i]+A[i+1])
    print(A)
    
staircase(8)
staircase(9)


# you could've allocated A with len(N+1) all elements 0 and use
# A[i+2]=A[i]+A[i+1]

def staircase(N=5):
    if N == 0 or N==1:
        return 1,
    
    A = [1]*(N+1)
    
    for i in range(N-1):
        A[i+2] = A[i]+A[i+1]
    print(A)

staircase(8)
staircase(9)

# What if we allow steps anything?


[Amazon Coding Interview Question - Recursive Staircase Problem] - https://youtu.be/5o-kdjv7FD0