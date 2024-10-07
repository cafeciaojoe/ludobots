#So far, we have named our files using verbs, indicating what they do: generate.py a world and robot, simulate.py them, and then analyze.py them.
# We will now create one file for each class, and we will use a noun to name it.

from world import WORLD
from robot import ROBOT

import pybullet as p
import numpy
import time
import pyrosim.pyrosim as pyrosim
#plane.urdf comes with pybullet; you do not have to generate it. We have to tell pybullet where to find it by adding
import pybullet_data
import os
import math
import random
import constants as c

#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

class SIMULATION:

    def __init__(self, directOrGUI):

        self.directOrGUI = directOrGUI

        if directOrGUI == "DIRECT":
            # running the sim "blind"
            self.physicsClient = p.connect(p.DIRECT)
        else:
            # running the sim "heads up"
            self.physicsClient = p.connect(p.GUI)

        # this line allows the use of an existing asset, ie a floor e.g. plane.udrf
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # to disable the sidebars on the pybullet simulation.
        # This change will also dramatically speed up the GUI simulation on some platforms.
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

        # ou will have noticed that if you manipulate the cube and then let it go, it will float away.
        # This is because no forces are currently at work in your simulated world.
        p.setGravity(c.Xgravity, c.Ygravity, c.Zgravity)

        self.world = WORLD()
        self.robot = ROBOT()

        # Pyrosim has to do some additional setting up when it is used to simulate sensors. So, add just before entering the for loop in simulate.py.
        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()


    def Run(self):
        loops = c.loops
        for t in range(0, loops):
            #print(i)
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.think()
            self.robot.Act(t)
            if self.directOrGUI == "GUI":
                time.sleep(c.loopSleep)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
        pass

    #https://www.geeksforgeeks.org/destructors-in-python/
    def __del__(self):
        #self.robot.Save_Values()
        p.disconnect()