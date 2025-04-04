#So far, we have named our files using verbs, indicating what they do: generate.py a world and robot, simulate.py them, and then analyze.py them.
# We will now create one file for each class, and we will use a noun to name it.

#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK

import os
import numpy as np

from sensor import SENSOR
from motor import MOTOR
import constants as c

class ROBOT:

    def __init__(self,solutionID):
        self.robotId = p.loadURDF(f"body{str(solutionID)}.urdf")
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        # kagi assistant said os.remove is safer and more pythonic than the rm shell command
        #os.remove(f"brain{solutionID}.nndf")

        self.LeftLowerLegValues = []
        self.RightLowerLegValues = []
        self.BackLowerLegValues = []
        self.FrontLowerLegValues = []

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
        for sensor_name, sensor in self.sensors.items():
            sensor.Get_Value(timeStep)
            if 'Lower' in sensor_name: #send all the lower leg values te be collected in a dict. 
                self.update_jump_fitness(sensor.sensorValues[timeStep],sensor_name)

        # original funciton
        # for sensor in self.sensors.values():
        #     sensor.Get_Value(timeStep)

    def think(self):
        self.nn.Update()
        #self.nn.Print()

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
        pass

    def Act(self, timeStep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                # so the value of the sensor gets propegated thru the network, multiplied by the weights,
                # as it dos it turns into an actual angle (in radians).
                # c.motorjointRange restricts this range to promote osciliatory motion in the locomotion solutions
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(desiredAngle, self)
                # print(f'the motor neuron name is: {neuronName}')
                # print(f'the motor neuron value is: {desiredAngle}')
                # print(f'the corresponding joint name is: {jointName}')

    # this should be called "export fitness" because when it is called nothing is done with the vlaue. 
    def Get_Fitness(self,solutionID):

        # these lines querie pyrosim for the position of the first link which is a leg
        # stateOfLinkZero = p.getLinkState(self.robotId, 0)
        # positionOfLinkZero = stateOfLinkZero[0]
        # xCoordinateOfLinkZero = positionOfLinkZero[0]

        # these lines querie pyrosim for the position of the base link which is the torso
        # basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        # basePosition = basePositionAndOrientation[0]
        # zPosition = basePosition[2]

        leftMean = np.mean(self.LeftLowerLegValues) if self.LeftLowerLegValues else 0
        rightMean = np.mean(self.RightLowerLegValues) if self.RightLowerLegValues else 0
        backMean = np.mean(self.BackLowerLegValues) if self.BackLowerLegValues else 0
        frontMean = np.mean(self.FrontLowerLegValues) if self.FrontLowerLegValues else 0

        # Calculate the mean of all four legs
        jumpMean = np.mean([leftMean, rightMean, backMean, frontMean])

        with open(f"tmp{solutionID}.txt", "w") as f:
            f.write(str(jumpMean))
            f.close()
        
        os.system(f"mv tmp{solutionID}.txt fitness{solutionID}.txt")

    def update_jump_fitness(self, sensor_value, sensor_name):
        if 'LeftLowerLeg' in sensor_name:
            self.LeftLowerLegValues.append(sensor_value)
        elif 'RightLowerLeg' in sensor_name:
            self.RightLowerLegValues.append(sensor_value)
        elif 'BackLowerLeg' in sensor_name:
            self.BackLowerLegValues.append(sensor_value)
        elif 'FrontLowerLeg' in sensor_name:
            self.FrontLowerLegValues.append(sensor_value)