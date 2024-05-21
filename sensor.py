#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import numpy
import pyrosim.pyrosim as pyrosim

class SENSOR:

    def __init__(self, linkname):
        self.linkName = linkname
        self.values = numpy.zeros(100)
        pass

    def Get_Value(self):
        self.values = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)