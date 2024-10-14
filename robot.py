#So far, we have named our files using verbs, indicating what they do: generate.py a world and robot, simulate.py them, and then analyze.py them.
# We will now create one file for each class, and we will use a noun to name it.

#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK

import os

from sensor import SENSOR
from motor import MOTOR

class ROBOT:

    def __init__(self,solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        os.system(f"rm brain{solutionID}.nndf")

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
        """
        the following attempt is wrong

        for i in self.sensors:
            self.sensors[i] = SENSOR.Get_Value(timeStep)
        pass

        The issue lies in the Sense method of your ROBOT class.
        Specifically, you are trying to call SENSOR.Get_Value(timeStep)
        as if it were a static method, but it is an instance method.
        You should call Get_Value on each instance of SENSOR stored in self.sensors.
        """

        for sensor in self.sensors.values():
            sensor.Get_Value(timeStep)

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
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(desiredAngle, self)
                # print(f'the motor neuron name is: {neuronName}')
                # print(f'the motor neuron value is: {desiredAngle}')
                # print(f'the corresponding joint name is: {jointName}')

    # this should be called "export fitness" because when it is called nothing is done with the vlaue. 
    def Get_Fitness(self,solutionID):
        # in 37 L "hll climber, self.robotId is reffered to as just self.robot
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        #print(stateOfLinkZero)
        #print(positionOfLinkZero[0])

        with open(f"tmp{solutionID}.txt", "w") as f:
            f.write(str(xCoordinateOfLinkZero))
            f.close()
        
        os.system(f"mv tmp{solutionID}.txt fitness{solutionID}.txt")

        #with open(f"fitness{solutionID}.txt", "w") as f:
        #    f.write(str(xCoordinateOfLinkZero))
        #    f.close()