import numpy as np

def windowize(arr, window):

    the_liste = []
    for cur in range(arr.shape[0] - window +1 ):
        the_liste.append(arr[cur:cur+window].reshape(1,window,-1))

    the_tensor = np.vstack(the_liste)

    return the_tensor

def windowize_explained():
    
    tensor = np.random.randint(1, 5, size=(5,4,3))
    x = tensor[:, 0, 0] # amount, store, sku
    x = x.reshape(-1, 1)
    # the code above was how we generated x in thesis
    # for simplicity we continue by just filling with increasing numbers
    x = np.arange(1,11).reshape(-1,1) 
    print('x:')
    print(x)
    print('windowize(x, 2):')
    print(windowize(x, 2))
    
    print('x.shape', x.shape)
    print('windowize(x, 2).shape', windowize(x, 2).shape)
    print('windowize(x, 3).shape', windowize(x, 3).shape)
    
    # After windowizing, number of samples = n_timepoints - window + 1
    # just ignore third dimension and notice first elements of pairs 1..9
    # [1,2] .. [9, 10]
    
windowize_explained()

# Working example for 1D backtest index splitting

def plain_backtest_split(n_timepoints, n_splits, split_no):
    
    indices = list(range(n_timepoints))
    n_folds = n_splits + 1

    # Because in a split, there is training and validation
    # In the first split, first fold is training; and second fold is validation
    # In the second split, first fold + second fold is training; and third fold is validation
    
    if n_folds > n_timepoints:
        raise ValueError('Cannot have number of n_folds > n_timepoints')
    
    fold_size = n_timepoints // n_folds
    print('fold_size:', fold_size)
    
    remainder = n_timepoints % n_folds
    
    print('remainder:', remainder)
    # this remainder will be added to first fold
    # therefore first fold may be greater than fold_size
    # however following folds are guaranteed to be fold_size long
    # yes, including the last fold, we will verify it later

    val_starts = range(fold_size + remainder, n_timepoints, fold_size)
    print('val_starts:', val_starts, '=', list(val_starts))
    
    val_start = val_starts[split_no-1]
    # this is just to adjust zero-based numbering; minimum split_no is 1
    
    print('val_start:', val_start)
    
    print(list(range(val_start)), list(range(val_start, val_start + fold_size)))
    
    #As seen; each fold is n_folds in length
    #And as seen, the first fold is exempt from this obligation
    
plain_backtest_split(n_timepoints=10, n_splits=2, split_no=1)
plain_backtest_split(n_timepoints=10, n_splits=2, split_no=2)
plain_backtest_split(n_timepoints=10, n_splits=5, split_no=1)

n_timepoints = 10
print('indices:', list(range(n_timepoints)))


# Working example for 3D backtest index splitting.
# It is used for correctly splitting windowized x on its 1 st dimension for train and validation 
# (9, 2, 1) -> (5, 2, 1) | (4, 2, 1)
# However, instead of windowizing and splitting, first split 1D version of x with possible intersections
# for example range(0, 6) | range(5, 10) = [0, 1, 2, 3, 4, 5] | [5, 6, 7, 8, 9]
# and then windowize those indices to [[0, 1], ..., [4, 5]] | [[5,6], ... , [8, 9]]
# so this 1D needs to be specialized version of plain_backtest_split in which folds were mutually exclusive
# actually, how much indices will intersect depends on window_size, so for example if window_size is 2, only 1 value 
# be in intersection. if window_size = 3, then 2 values in intersection ... so on.
# why do we let train/validation intersect ? indeed we must let them intersect in a way that when windowized,
# train and validation follow each other smoothly. see above: the last element of train indices [4, 5] 
# and the first element of validation is [5, 6]. see that smallest elements in those windows are consecutive.
# smallest element in first window of validation, is the smallest element in its 1D split, by the nature of windowizing.
# largest element in the last window of train, is the largest element in its 1D split, by the nature of windowizing.
# also, there is a fixed relation between largest and smallest elements in any window. 
# that is, smallest = largest - window_size + 1
# Putting it all together, 
#                          validation smallest = train.largest - window_size + 1 + 1
#						   validation smallest = train.largest - window_size + 2
# 
# Finally, to clearly understand array bounds, in for loop if you just ignore "window - 1" parts, it becomes 1D plain_backtest_split
# as if it is done on len(n_samples) array, i.e. [0, 1, 2, ..., 8]
# remember that preliminary array was [0, 1, 2, ..., 9]
# when "window - 1" is added to slice stop values; (i) for validation part last element coincides with preliminary array's last element
# (ii) for training part it is still within arrays boundary, so it doesn't pose a problem
 

def get_splits(n_timepoints, window, n_splits, cur_split):
    
    indices = np.arange(n_timepoints)    

    n_samples  = n_timepoints - window + 1
    n_folds = n_splits + 1

	if n_folds > n_samples:
        raise ValueError('Cannot have number of n_folds > n_samples')

  
    val_size = n_samples // n_folds
    remainder = n_samples % n_folds

    val_starts = range(val_size + remainder, n_samples, val_size)

    indices_list = []
    for val_start in val_starts:
        indices_list.append(( indices[: val_start + window - 1], indices[ val_start: val_start + window - 1 + val_size]))
        
    return indices_list[cur_split]
