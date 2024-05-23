#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import numpy
import pyrosim.pyrosim as pyrosim
import constraints as c

class SENSOR:

    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.loops)
        pass

    def Get_Value(self,timeStep):
        self.values[timeStep] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        if timeStep >= c.loops-1:
            print(self.values)