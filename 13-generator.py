##############################################
## Generator for out-of-core learning.
## Out-of-core learning is a set of algorithms working with data that cannot 
## fit into the memory of a single computer, but that can easily 
## fit into a local hard disk or web repository.
##############################################

# Inputs:
# values [0, 10, 20, 30, 40]
# batch_size 2
#
# len(gen) 3
# gen[0] [0, 10]
# gen[1] [20, 30]
# gen[2] [40] 
# gen[3] # throws IndexError because we handled that case
# Python says you need to handle illegal indices and throw IndexError
# Inside a member method, len(self) and self.__len__() works the same
#
# An iteration understands from IndexError that a loop should be finished
# and we dont see any errors, it works correctly
# [i for i in gen] [[0, 10], [20, 30], [40]]

# Working example # 1, returns premature chunk, no shuffle
class DataGenerator():
    
    def __init__(self, values, batch_size, shuffle=True):

        self.batch_size = batch_size
        self.values = values
        self.shuffle = shuffle

    def __len__(self):
        # Number of chunks
        return int( np.ceil( len( self.values ) / self.batch_size) )
    
    def __getitem__(self, index):

        if index>=len(self):
            raise IndexError()
            
        # Generate one chunk
        return values[index*self.batch_size: (index+1)*self.batch_size]

values = [10, 20, 30, 40, 50]   

gen = DataGenerator(values=values, batch_size=2)

print(len(gen))
print(gen[0]) # [0, 10]
print(gen[1]) # [20, 30]
print(gen[2]) # [40]
print(gen[2]) # Throws IndexError
print([i for i in gen]) # [[0, 10], [20, 30], [40]]


# values [0, 10, 20, 30, 40]
# batch_size 2
#
# First epoch
# len(gen) 3
# gen.indices [1 3 2 0 4]
# chunks [10, 30] [20, 0] [40]
# gen.on_epoch_end()
# Second epoch
# gen.indices [4 2 0 1 3]
# chunks [40, 20] [0, 10] [30]
#
# We could also ignore premature chunk, by floor-ing instead of ceil-ing
# since we shuffle in each epoch, sooner or later each training sample will be in a chunk

# Working example # 2, returns premature chunk, shuffle
class DataGenerator():
    
    def __init__(self, values, batch_size, shuffle=True):

        self.values = values
        self.indices = np.arange(len(values))
        self.batch_size = batch_size
        self.shuffle = shuffle

        if shuffle:
            np.random.shuffle(self.indices)
    
    def on_epoch_end(self):
        
        self.indices = np.arange(len(self.values))
        
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __len__(self):
        
        return int( np.ceil( len( self.values ) / self.batch_size) )
    
    def __getitem__(self, index):

        if index >= len(self):
            raise IndexError()
        
        indices_chunk = self.indices[index * self.batch_size: (index + 1) * self.batch_size]
        values_chunk = [self.values[i] for i in indices_chunk]
        return values_chunk

values = [0, 10, 20, 30, 40]

gen = DataGenerator(values=values, batch_size=2, shuffle=True)

print(len(gen))
print('values', gen.values)
print(gen.indices)
print(gen[0], gen[1], gen[2])
gen.on_epoch_end()
print(gen.indices)
print(gen[0], gen[1], gen[2])


# Reference
# https://stackoverflow.com/a/51709835