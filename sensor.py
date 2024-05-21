#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import numpy
import pyrosim.pyrosim as pyrosim

class SENSOR:

    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(100)
        pass

    def Get_Value(self,timeStep):
        self.values[timeStep] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        print(self.values)