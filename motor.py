#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import numpy

import pyrosim.pyrosim as pyrosim
import constraints as c

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.values = numpy.zeros(c.loops)
        pass