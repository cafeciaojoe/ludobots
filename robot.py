#So far, we have named our files using verbs, indicating what they do: generate.py a world and robot, simulate.py them, and then analyze.py them.
# We will now create one file for each class, and we will use a noun to name it.

#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import pybullet as p
import pyrosim.pyrosim as pyrosim

from sensor import SENSOR
from motor import MOTOR

class ROBOT:

    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        #Note: linkNamesToIndices is a dictionary used inside of pyrosim to hide a
        # lot of details from you. But, for this, we will use it to give us the name
        # of every link in body.urdf. Verify this by running simulate.py.
        # You should see three names printed.
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        pass

    def Sense(self, timeStep):
        # The issue lies in the Sense method of your ROBOT class.
        # Specifically, you are trying to call SENSOR.Get_Value(timeStep)
        # as if it were a static method, but it is an instance method.
        # You should call Get_Value on each instance of SENSOR stored in self.sensors.
        # for i in self.sensors:
        #     self.sensors[i] = SENSOR.Get_Value(timeStep)
        # pass

        for sensor in self.sensors.values():
            sensor.Get_Value(timeStep)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
        pass

    def Act(self):
        for motor in self.motors.values():
            motor.Set_Value()
        pass