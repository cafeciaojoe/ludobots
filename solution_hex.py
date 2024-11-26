import numpy
import pyrosim.pyrosim as pyrosim
import random
import os
import time

import constants as c

"""Note that the weights matrix should be taller than it is wide (three rows and two columns). If you want the weight
 of the synapse that connects the third sensor neuron to the second motor neuron, for example, you would "walk down" 
 to the third row, and then "walk right" to the second column."""

"""Note multiply this whole matrix by two and subtract one to scale each weight to the range [-1,+1]. Store it back in 
the same variable. Note that you do not have to do so by creating two nested for loops and performing element-wise 
operations. Instead, you can do this in just one line with self.weights * 2 - 1. When you do the latter, you are 
performing vector operations."""

class SOLUTION():
    def __init__(self,nextAvailableID):
        #Create an array of the given shape (n dimensions) and populate it with random samples from a uniform distribution over [0, 1).
        self.weights = numpy.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        # multiply this whole matrix by two and subtract one to scale each weight to the range [-1,+1]. Store it back in the same variable. 
        # Note that you do not have to do so by creating two nested for loops and performing element-wise operations. Instead, you can do 
        # this in just one line with self.weights * 2 - 1. When you do the latter, you are performing vector operations.
        self.weights = self.weights*2-1
        self.myID = nextAvailableID
        pass

    def Start_Simulation(self,directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        # TODO: try to do run simulate.py differently because it is hard to debug. 
        #if self.myID > 10:
        #    exit()

        """ i am still not sure why this is run seperately and not imported as a module 
        # i guess you dont need an instance of SIMULATION with every deep copy of HILL_CLIMBER"""

        # adding "&" runs simulate.py as a background process

        os.system(f"python3 simulate.py {directOrGUI} {self.myID} &")

        # adding 2&>1 & supresses any warnign messages
        #os.system(f"python3 simulate.py {directOrGUI} {self.myID} 2&>1 &")

        

    def Wait_For_Simulation_To_End(self):
        # delay the read in of fitness .txt until it has been created by simulate.py
        while not os.path.exists(f"fitness{str(self.myID)}.txt"):
            time.sleep(0.01)

        with open(f"fitness{str(self.myID)}.txt", "r") as f:
            self.fitness = float(f.read())
            #print(self.fitness)
            f.close()
        
        # kagi assistant said os.remove is safer and more pythonic than the rm shell command
        #TODO make a seperate folder where these go so the root is not so populated with these files duing big sims. 
        os.remove(f"fitness{str(self.myID)}.txt")
        os.remove(f"body{str(self.myID)}.urdf")
        os.remove(f"world{str(self.myID)}.sdf")
        os.remove(f"brain{str(self.myID)}.nndf")

    def Create_World(self):
        pyrosim.Start_SDF(f"world{str(self.myID)}.sdf")
        length = 1
        width = 1
        height = 1
        #pyrosim.Send_Cube(name="Box", pos=[-3, -3, height / 2], size=[length, width, height])
        pyrosim.End()

    # reffered to as Send_Body() in step 29 of quadruped. 
    def Create_Body(self):
        # Joints with no upstream joint have absolute positions. Every other joint has a position relative to its upstream joint.
        # so both of these joints need to be absolute!!!
        # https://docs.google.com/presentation/d/1zvZzFyTf8PBNjzQZx_gZk84aUntZo2bUKhpe78yT4OY/edit#slide=id.g10dad2fba23_2_371
        pyrosim.Start_URDF(f"body{str(self.myID)}.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 2, 1])

        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0, 0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0, 1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0, -0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1.0, 0.2])
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0, -1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_FrontLeftLeg", parent="Torso", child="FrontLeftLeg", type="revolute", position=[-0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="FrontLeftLeg", pos=[-0.5, .5, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="FrontLeftLeg_FrontLeftLowerLeg", parent="FrontLeftLeg", child="FrontLeftLowerLeg", type="revolute", position=[-1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="FrontLeftLowerLeg", pos=[0, 0.5, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_BackLeftLeg", parent="Torso", child="BackLeftLeg", type="revolute", position=[-0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="BackLeftLeg", pos=[-0.5, -0.5, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="BackLeftLeg_BackLeftLowerLeg", parent="BackLeftLeg", child="BackLeftLowerLeg", type="revolute", position=[-1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="BackLeftLowerLeg", pos=[0, -0.5, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_FrontRightLeg", parent="Torso", child="FrontRightLeg", type="revolute", position=[0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="FrontRightLeg", pos=[0.5, 0.5, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="FrontRightLeg_FrontRightLowerLeg", parent="FrontRightLeg", child="FrontRightLowerLeg", type="revolute", position=[1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="FrontRightLowerLeg", pos=[0, 0.5, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_BackRightLeg", parent="Torso", child="BackRightLeg", type="revolute", position=[0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="BackRightLeg", pos=[0.5, -0.5, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="BackRightLeg_BackRightLowerLeg", parent="BackRightLeg", child="BackRightLowerLeg", type="revolute", position=[1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="BackRightLowerLeg", pos=[0, -0.5, -0.5], size=[0.2, 0.2, 1])
        pyrosim.End()
        

    # this function is reffered to as "Send_Brain()" in step 34 of ParralellHillClimber
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name= '0', linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name= '1', linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name= '2', linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name= '3', linkName="BackLeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name= '4', linkName="BackRightLowerLeg")
        pyrosim.Send_Sensor_Neuron(name= '5', linkName="FrontLeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name= '6', linkName="FrontRightLowerLeg")

        pyrosim.Send_Motor_Neuron(name= '7', jointName='Torso_FrontLeg')
        pyrosim.Send_Motor_Neuron(name= '8', jointName='Torso_BackLeg')
        pyrosim.Send_Motor_Neuron(name= '9', jointName='BackLeftLeg_BackLeftLowerLeg')
        pyrosim.Send_Motor_Neuron(name= '10', jointName='FrontLeg_FrontLowerLeg')
        pyrosim.Send_Motor_Neuron(name= '11', jointName='BackLeg_BackLowerLeg')
        pyrosim.Send_Motor_Neuron(name= '12', jointName='BackRightLeg_BackRightLowerLeg')
        pyrosim.Send_Motor_Neuron(name= '13', jointName='FrontRightLeg_FrontRightLowerLeg')
        pyrosim.Send_Motor_Neuron(name= '14', jointName='FrontLeftLeg_FrontLeftLowerLeg')
        pyrosim.Send_Motor_Neuron(name= '15', jointName='Torso_FrontLeftLeg')
        pyrosim.Send_Motor_Neuron(name= '16', jointName='Torso_FrontRightLeg')

        first_motor_neuron = c.numSensorNeurons - 1

        #2 x 3 = 6 synapses. each motor connected to each neuron.
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(
                    sourceNeuronName=str(currentRow),
                    targetNeuronName=str(currentColumn + first_motor_neuron),
                    weight=self.weights[currentRow, currentColumn]
                )

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons -1)
        randomColumn = random.randint(0,c.numMotorNeurons -1)
        self.weights[randomRow,randomColumn] = random.random()*2-1

    # used for assigning uniques ID to newly spawned children
    def setID(self,nextAvailableID):
        self.myID = nextAvailableID

if __name__ == '__main__':
    nextAvailableID = 0  
    solution = SOLUTION(nextAvailableID)
    solution.Start_Simulation('GUI')  