# Solution 1 brute force, O(n^3) time
# since solution set must not contain duplicate triplets,
# I took care of adding by using set, sort and tuple tools

class Solution:
    
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        if len(nums)<3:
            return []

        res = set()
        
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                for k in range(j+1, len(nums)):
                    
                    if nums[i] + nums[j] + nums[k] == 0:
                        res.add(tuple(sorted([nums[i], nums[j], nums[k]])))
        
        return list(res)


# (1) 
# if we find a solution for i
# dont break 
# instead look for other j,k 
# thats why k -=1 
# note that other j +=1 at works the same
#
# (2)
# we are preemptively skipping j,k for duplicates
# so that for each i, if we calculate cur
# next A[j] will be certainly different from current A[j]
# next A[k] will be certainly different from current A[k]
# 
# (3)
# however we dont preemptively skip i for duplicates
# if we calculate cur
# next A[i] can be equal to cur A[i]
# thats because if A=[1,1,1] and target=3 we want to allow
# A[i] == A[j] and A[i] == A[k]
#
# if we are done with an i, we skip next duplicates
# so if we use an i, it is the lowest position among its duplicates
#
# extra info: if A[i] != A[j] certainly A[i] != A[k]
# because A is sorted

def solution3Sum(A = [0,1,1,2,3,7,8,8,9,14,15], target=17):
    
    A = sorted(A) # O(nlogn)
    
    i=0

    while i<len(A)-2:

        if i==0 or (i>0 and A[i-1] != A[i]): #(3)
            k = len(A)-1
            j = i+1

            while j<k:
                #print(i,j,k)
                while A[k]==A[k-1]: k -= 1 #(2)
                while A[j]==A[j+1]: j += 1 #(2)

                cur = A[i]+A[j]+A[k]

                if cur==target:
                    print('found',i,j,k)
                    k -= 1 #(1)
                    #j += 1
                elif cur>target:
                    k -= 1
                else:
                    j += 1

        i += 1
        
solution3Sum(A = [0,1,1,3,5,7], target=8)
# found 0 2 5
# found 0 3 4
print()

solution3Sum(A = [0,1,1,3,5,7], target=6)
# found 0 2 4
print()

solution3Sum(A = [0,1,1,2,3,7,8,8,9,14,15], target=15)
# found 0 2 9
# found 0 5 6


# 15. 3Sum
# https://leetcode.com/problems/3sum/