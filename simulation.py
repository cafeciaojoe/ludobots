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
import constraints as c

#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

class SIMULATION:

    def __init__(self):
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

    def run(self):
        loops = c.loops
        for i in range(1, loops):
            print(i)
            p.stepSimulation()
            # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            # # print(backLegSensorValues[i],frontLegSensorValues[i])
            #
            # # During each step of the simulation, we are going to simulate a motor that supplies force to one of the robot's joints. To do so, add this statement
            # pyrosim.Set_Motor_For_Joint(
            #
            #     bodyIndex=robotId,
            #
            #     jointName="Torso_FrontLeg",
            #
            #     controlMode=p.POSITION_CONTROL,
            #
            #     # the desired angle between the two links connected by the joint
            #     targetPosition=frontLegTargetAngles[i],
            #
            #     maxForce=c.frontLegForceMax)
            #
            # pyrosim.Set_Motor_For_Joint(
            #
            #     bodyIndex=robotId,
            #
            #     jointName="Torso_BackLeg",
            #
            #     controlMode=p.POSITION_CONTROL,
            #
            #     # the desired angle between the two links connected by the joint
            #     targetPosition=backLegTargetAngles[i],
            #
            #     maxForce=c.frontLegForceMax)
            #
            time.sleep(c.loopSleep)

    #https://www.geeksforgeeks.org/destructors-in-python/
    def __del__(self):
        p.disconnect()