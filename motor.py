#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import numpy

import pyrosim.pyrosim as pyrosim
import constants as c

import pybullet as p

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.motorValues = numpy.zeros(c.loops)
        self.Prepare_To_Act()
        pass

    def Prepare_To_Act(self):
        # The Prepare_To_Act method in the MOTOR class is more specific.
        # It prepares an individual motor for action. This could involve
        # initializing motor-specific parameters such as amplitude, frequency,
        # and phase offset, and setting up any internal data structures needed for motor control.

        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.offset = c.offset

        #not needed maybe?
        self.TargetAngleMin = c.TargetAngleMin
        self.TargetAngleMax = c.TargetAngleMax

        self.motorValues = self.amplitude * numpy.sin(
            self.frequency * numpy.linspace(self.TargetAngleMin, self.TargetAngleMax, num=c.loops,
                                         endpoint=True) + self.offset)

        # print(id(self),self.motorValues)
        #
        # self.frontLegTargetAngles = self.amplitude * numpy.sin(
        #     self.frequency * numpy.linspace(self.TargetAngleMin, self.TargetAngleMax, num=c.loops,
        #                                  endpoint=True) + self.offset)
        # self.backLegTargetAngles = c.amplitude * numpy.sin(
        #     c.frequency * numpy.linspace(self.TargetAngleMin, self.TargetAngleMax, num=c.loops,
        #                                  endpoint=True) + self.offset)

    def Set_Value(self, timeStep, robot):
        #print('set_value timestep and robot id',timeStep, robot)
        pyrosim.Set_Motor_For_Joint(

            bodyIndex=robot.robotId,

            jointName=self.jointName,

            controlMode=p.POSITION_CONTROL,

            # the desired angle between the two links connected by the joint
            targetPosition = self.motorValues[timeStep],
            #targetLocation = self.motorValues[timeStep],

            maxForce=c.frontLegForceMax)

        pass

