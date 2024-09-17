"""what is in the world"""

"""This file will use pyrosim to generate a link (later, several links comprising the world),
store it in a special file called world.sdf, and
simulate.py will then read it in and simulate it.
"""

import pyrosim.pyrosim as pyrosim
import random


length = 1
width = 1
height = 1


def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-3, -3, height/2], size=[length, width, height])
    pyrosim.End()

def Create_Robot():
    pass

def Generate_Brian():
    """Note: urdf files are a broadly-used file format in the robotics community. nndf files, in contrast,
    are specific to pyrosim, our in-house python robotics simulator. nndf files are designed to shorten the
    time it takes you to simulate a neural network-controlled robot."""

    pyrosim.Start_NeuralNetwork("brain.nndf")

    # Define sensor neurons
    sensor_neurons = [0, 1, 2]
    for i, link_name in enumerate(["Torso", "BackLeg", "FrontLeg"]):
        pyrosim.Send_Sensor_Neuron(name=sensor_neurons[i], linkName=link_name)

    # Define motor neurons
    motor_neurons = [3, 4]
    motor_joints = ["Torso_BackLeg", "Torso_FrontLeg"]
    for i, joint_name in enumerate(motor_joints):
        pyrosim.Send_Motor_Neuron(name=motor_neurons[i], jointName=joint_name)

    # Create synapses between each sensor neuron and each motor neuron
    for sensor in sensor_neurons:
        for motor in motor_neurons:

            pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight=random.uniform(-1,1))

    pyrosim.End()


def Generate_Body():
    #Joints with no upstream joint have absolute positions. Every other joint has a position relative to its upstream joint.
    #so both of these joints need to be absolute!!!
    #https://docs.google.com/presentation/d/1zvZzFyTf8PBNjzQZx_gZk84aUntZo2bUKhpe78yT4OY/edit#slide=id.g10dad2fba23_2_371
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[1,1,1])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1,0,1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-.5,0,-.5], size=[1,1,1])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2,0,1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[.5,0,-.5], size=[1,1,1])
    pyrosim.End()

Create_World()
Generate_Body()
Generate_Brian()