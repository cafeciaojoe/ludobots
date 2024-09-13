"""what is in the world"""

"""This file will use pyrosim to generate a link (later, several links comprising the world),
store it in a special file called world.sdf, and
simulate.py will then read it in and simulate it.
"""

import pyrosim.pyrosim as pyrosim

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

    """As the name implies, sensor neurons receive values from sensors. We are going to name our neurons with numbers, 
    because we are going to update the values of each neuron in our neural network, every simulation time step, in a 
    specific order: sensor neurons first, hidden neurons next, and finally motor neurons.
    This particular neuron is going to receive a value from sensor stored in Torso."""

    # sensors and sensor neurons go on links
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

    # motors and motor neurons go on joints
    # note: Note that this motor neuron will send values to the motor controlling joint Torso_BackLeg
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=4, weight=1.0)
    pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=2.0)
    pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=4, weight=3.0)
    pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=4, weight=1.0)
    pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=2.0)
    pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=4, weight=3.0)
    pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=4, weight=1.0)
    pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=2.0)
    pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=4, weight=3.0)
    pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=4, weight=1.0)
    pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=2.0)
    pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=4, weight=3.0)




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