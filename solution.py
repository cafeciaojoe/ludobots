import numpy
import pyrosim.pyrosim as pyrosim
import random
import  os


"""Note that the weights matrix should be taller than it is wide (three rows and two columns). If you want the weight
 of the synapse that connects the third sensor neuron to the second motor neuron, for example, you would "walk down" 
 to the third row, and then "walk right" to the second column."""

"""Note multiply this whole matrix by two and subtract one to scale each weight to the range [-1,+1]. Store it back in 
the same variable. Note that you do not have to do so by creating two nested for loops and performing element-wise 
operations. Instead, you can do this in just one line with self.weights * 2 - 1. When you do the latter, you are 
performing vector operations."""

class SOLUTION():
    def __init__(self):
        #Create an array of the given shape (n dimensions) and populate it with random samples from a uniform distribution over [0, 1).
        self.weights = numpy.random.rand(3,2)
        # multiply this whole matrix by two and subtract one to scale each weight to the range [-1,+1]. Store it back in the same variable. 
        # Note that you do not have to do so by creating two nested for loops and performing element-wise operations. Instead, you can do 
        # this in just one line with self.weights * 2 - 1. When you do the latter, you are performing vector operations.
        self.weights = self.weights*2-1
        pass

    def Evaluate(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        # i am still not sure why this is run seperately and not imported as a module 
        # i guess you dont need an instance of SIMULATION with every deep copy of HILL_CLIMBER
        os.system("python3 simulate.py DIRECT")
        with open("fitness.txt", "r") as f:
            self.fitness = float(f.read())
            f.close()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        length = 1
        width = 1
        height = 1
        pyrosim.Send_Cube(name="Box", pos=[-3, -3, height / 2], size=[length, width, height])
        pyrosim.End()

    def Create_Body(self):
        # Joints with no upstream joint have absolute positions. Every other joint has a position relative to its upstream joint.
        # so both of these joints need to be absolute!!!
        # https://docs.google.com/presentation/d/1zvZzFyTf8PBNjzQZx_gZk84aUntZo2bUKhpe78yT4OY/edit#slide=id.g10dad2fba23_2_371
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1, 0, 1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-.5, 0, -.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2, 0, 1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name= '0', linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name= '1', linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name= '2', linkName="FrontLeg")
        pyrosim.Send_Motor_Neuron(name= '3', jointName='Torso_BackLeg')
        pyrosim.Send_Motor_Neuron(name= '4', jointName='Torso_FrontLeg')

        num_sensor_neurons = 2
        num_motor_neurons = 3
        first_motor_neurons = num_sensor_neurons +1

        #2 x 3 = 6 synapses. each motor connected to each neuron.
        for currentRow in range(num_motor_neurons):
            for currentColumn in range(num_sensor_neurons):
                pyrosim.Send_Synapse(
                    sourceNeuronName=str(currentRow),
                    targetNeuronName=str(currentColumn + first_motor_neurons),
                    weight=self.weights[currentRow, currentColumn]
                )

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,2)
        randomColumn = random.randint(0,1)
        self.weights[randomRow,randomColumn] = random.random()*2-1
