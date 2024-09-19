import numpy

"""Note that the weights matrix should be taller than it is wide (three rows and two columns). If you want the weight
 of the synapse that connects the third sensor neuron to the second motor neuron, for example, you would "walk down" 
 to the third row, and then "walk right" to the second column."""

"""Note multiply this whole matrix by two and subtract one to scale each weight to the range [-1,+1]. Store it back in 
the same variable. Note that you do not have to do so by creating two nested for loops and performing element-wise 
operations. Instead, you can do this in just one line with self.weights * 2 - 1. When you do the latter, you are 
performing vector operations."""

class SOLUTION():
    def __init__(self):
        #Create an array of the given shape (n dimensions) and populate it with random samples from a uniform distribution over [0, 1).
        self.weights = numpy.random.rand(3,2)
        print(self.weights)
        self.weights= self.weights*2-1
        print(self.weights)
        exit()
        pass