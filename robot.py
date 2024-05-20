#So far, we have named our files using verbs, indicating what they do: generate.py a world and robot, simulate.py them, and then analyze.py them.
# We will now create one file for each class, and we will use a noun to name it.

#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import pybullet as p
import pyrosim.pyrosim as pyrosim

class ROBOT:

    def __init__(self):

        self.motors = {}

        self.robotId = p.loadURDF("body.urdf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            print(linkName)
        pass
