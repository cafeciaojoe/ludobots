#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import numpy

import pyrosim.pyrosim as pyrosim
import constants as c
import pybullet as p

import os

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.motorValues = numpy.zeros(c.loops)
        pass

    def Set_Value(self, desiredAngle, robot):
        #print('set_value timestep and robot id',timeStep, robot)
        pyrosim.Set_Motor_For_Joint(

            bodyIndex=robot.robotId,

            jointName=self.jointName,

            controlMode=p.POSITION_CONTROL,

            # the desired angle between the two links connected by the joint
            targetPosition = desiredAngle,
            #targetLocation = self.motorValues[timeStep],

            maxForce=c.frontLegForceMax)

    # def Save_Values(self):
    #     print('saving ', self.jointName, ' motor values')
    #     numpy.save(os.path.join('data', (self.jointName + '_motor')), self.motorValues)

