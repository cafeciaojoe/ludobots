#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import numpy
import pyrosim.pyrosim as pyrosim
import constants as c

import os

class SENSOR:

    def __init__(self, linkName):
        self.linkName = linkName
        self.sensorValues = numpy.zeros(c.loops)
        pass

    def Get_Value(self,timeStep):
        self.sensorValues[timeStep] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        # at the end of the loop print all the recorded sensor values
        # TODO I dont know why we are not justs saving the file at the end of the loops, seems more elegant that make a "save_values" function3
        # if timeStep >= c.loops-1:
        #     print(self.values)

    def Save_Values(self):
        print('saving ', self.linkName, ' sensor values')
        numpy.save(os.path.join('data', (self.linkName + '_sensor')), self.sensorValues)