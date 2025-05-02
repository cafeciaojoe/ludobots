# So far, we have named our files using verbs, indicating what they do: generate.py a world and robot, simulate.py them, and then analyze.py them.
# We will now create one file for each class, and we will use a noun to name it.

# Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK

import os
import numpy as np

from sensor import SENSOR
from motor import MOTOR
import constants as c

class ROBOT:

    def __init__(self, solutionID):
        self.robotId = p.loadURDF(f"body{str(solutionID)}.urdf")
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        # kagi assistant said os.remove is safer and more pythonic than the rm shell command
        # os.remove(f"brain{solutionID}.nndf")
        
        # Initialize touchSensorValues as a dictionary
        self.touchSensorValues = {
            'LeftLowerLeg': [],
            'RightLowerLeg': [],
            'BackLowerLeg': [],
            'FrontLowerLeg': [],
            'LeftLeg': [],
            'RightLeg': [],
            'BackLeg': [],
            'FrontLeg': [],
            'Torso': []
        }

    def Prepare_To_Sense(self):
        self.sensors = {}
        # Note: linkNamesToIndices is a dictionary used inside of pyrosim to hide a
        # lot of details from you. But, for this, we will use it to give us the name
        # of every link in body.urdf. Verify this by running simulate.py.
        # You should see three names printed.
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        pass

    def Sense(self, timeStep):
        for sensor_name, sensor in self.sensors.items():
            sensor.Get_Value(timeStep)
            if 'LeftLowerLeg' in sensor_name:
                self.touchSensorValues['LeftLowerLeg'].append(sensor.sensorValues[timeStep])
            elif 'RightLowerLeg' in sensor_name:
                self.touchSensorValues['RightLowerLeg'].append(sensor.sensorValues[timeStep])
            elif 'BackLowerLeg' in sensor_name:
                self.touchSensorValues['BackLowerLeg'].append(sensor.sensorValues[timeStep])
            elif 'FrontLowerLeg' in sensor_name:
                self.touchSensorValues['FrontLowerLeg'].append(sensor.sensorValues[timeStep])
            elif 'LeftLeg' in sensor_name:
                self.touchSensorValues['LeftLeg'].append(sensor.sensorValues[timeStep])
            elif 'RightLeg' in sensor_name:
                self.touchSensorValues['RightLeg'].append(sensor.sensorValues[timeStep])
            elif 'BackLeg' in sensor_name:
                self.touchSensorValues['BackLeg'].append(sensor.sensorValues[timeStep])
            elif 'FrontLeg' in sensor_name:
                self.touchSensorValues['FrontLeg'].append(sensor.sensorValues[timeStep])
            elif 'Torso' in sensor_name:
                self.touchSensorValues['Torso'].append(sensor.sensorValues[timeStep])
                #print(f'Torso = {sensor.sensorValues[timeStep]}')
        # original function
        # for sensor in self.sensors.values():
        #     sensor.Get_Value(timeStep)

    def think(self):
        self.nn.Update()
        # self.nn.Print()

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
        pass

    def Act(self, timeStep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                # so the value of the sensor gets propagated through the network, multiplied by the weights,
                # as it does it turns into an actual angle (in radians).
                # c.motorjointRange restricts this range to promote oscillatory motion in the locomotion solutions
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(desiredAngle, self)
                # print(f'the motor neuron name is: {neuronName}')
                # print(f'the motor neuron value is: {desiredAngle}')
                # print(f'the corresponding joint name is: {jointName}')

    # this should be called "export fitness" because when it is called nothing is done with the value. 
    def Get_Fitness(self, solutionID):
        sit_phase = 0
        # Use all limb and torso sensor arrays for min_length
        min_length = min(
            len(self.touchSensorValues['LeftLowerLeg']),
            len(self.touchSensorValues['RightLowerLeg']),
            len(self.touchSensorValues['BackLowerLeg']),
            len(self.touchSensorValues['FrontLowerLeg']),
            len(self.touchSensorValues['LeftLeg']),
            len(self.touchSensorValues['RightLeg']),
            len(self.touchSensorValues['BackLeg']),
            len(self.touchSensorValues['FrontLeg']),
            len(self.touchSensorValues['Torso'])
        )

        for t in range(min_length):
            if (
                self.touchSensorValues['LeftLowerLeg'][t] == -1 and
                self.touchSensorValues['RightLowerLeg'][t] == -1 and
                self.touchSensorValues['BackLowerLeg'][t] == -1 and
                self.touchSensorValues['FrontLowerLeg'][t] == -1 and
                self.touchSensorValues['LeftLeg'][t] == -1 and
                self.touchSensorValues['RightLeg'][t] == -1 and
                self.touchSensorValues['BackLeg'][t] == -1 and
                self.touchSensorValues['FrontLeg'][t] == -1 and
                self.touchSensorValues['Torso'][t] == 1
            ):
                sit_phase += 1
            else:
                sit_phase = 0  # Reset if any limb or torso touches the ground

        # Write the sit phase duration to the fitness file
        with open(f"tmp{solutionID}.txt", "w") as f:
            f.write(str(sit_phase))
            f.close()
        
        os.system(f"mv tmp{solutionID}.txt fitness{solutionID}.txt")