#So far, we have named our files using verbs, indicating what they do: generate.py a world and robot, simulate.py them, and then analyze.py them.
# We will now create one file for each class, and we will use a noun to name it.

#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import pybullet as p
import pyrosim.pyrosim as pyrosim

from sensor import SENSOR

class ROBOT:

    def __init__(self):

        self.motors = {}

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

    def Sense(self):


        pass
