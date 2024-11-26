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
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[2, 2, 1])

        pyrosim.Send_Joint(name="Torso_Leg1", parent="Torso", child="Leg1", type="revolute", position=[-.5, 0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="Leg1", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Leg1_LowerLeg1", parent="Leg1", child="LowerLeg1", type="revolute", position=[0, 1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LowerLeg1", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_Leg2", parent="Torso", child="Leg2", type="revolute", position=[0.5, 0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="Leg2", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Leg2_LowerLeg2", parent="Leg2", child="LowerLeg2", type="revolute", position=[0, 1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LowerLeg2", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_Leg3", parent="Torso", child="Leg3", type="revolute", position=[-0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg3", pos=[-0.5, .5, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Leg3_LowerLeg3", parent="Leg3", child="LowerLeg3", type="revolute", position=[-1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LowerLeg3", pos=[0, 0.5, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_Leg4", parent="Torso", child="Leg4", type="revolute", position=[-0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg4", pos=[-0.5, -0.5, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Leg4_LowerLeg4", parent="Leg4", child="LowerLeg4", type="revolute", position=[-1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LowerLeg4", pos=[0, -0.5, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_Leg5", parent="Torso", child="Leg5", type="revolute", position=[0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg5", pos=[0.5, 0.5, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Leg5_LowerLeg5", parent="Leg5", child="LowerLeg5", type="revolute", position=[1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LowerLeg5", pos=[0, 0.5, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_Leg6", parent="Torso", child="Leg6", type="revolute", position=[0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg6", pos=[0.5, -0.5, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Leg6_LowerLeg6", parent="Leg6", child="LowerLeg6", type="revolute", position=[1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LowerLeg6", pos=[0, -0.5, -0.5], size=[0.2, 0.2, 1])
        
        pyrosim.Send_Joint(name="Torso_Leg7", parent="Torso", child="Leg7", type="revolute", position=[-0.5, -0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="Leg7", pos=[0, -0.5, 0], size=[0.2, 1.0, 0.2])
        pyrosim.Send_Joint(name="Leg7_LowerLeg7", parent="Leg7", child="LowerLeg7", type="revolute", position=[0, -1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LowerLeg7", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="Torso_Leg8", parent="Torso", child="Leg8", type="revolute", position=[0.5, -0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="Leg8", pos=[0, -0.5, 0], size=[0.2, 1.0, 0.2])
        pyrosim.Send_Joint(name="Leg8_LowerLeg8", parent="Leg8", child="LowerLeg8", type="revolute", position=[0, -1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LowerLeg8", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        
        pyrosim.End()
        

    # this function is reffered to as "Send_Brain()" in step 34 of ParralellHillClimber
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name= '0', linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name= '1', linkName="LowerLeg1")
        pyrosim.Send_Sensor_Neuron(name= '2', linkName="LowerLeg2")
        pyrosim.Send_Sensor_Neuron(name= '3', linkName="LowerLeg4")
        pyrosim.Send_Sensor_Neuron(name= '4', linkName="LowerLeg6")
        pyrosim.Send_Sensor_Neuron(name= '5', linkName="LowerLeg3")
        pyrosim.Send_Sensor_Neuron(name= '6', linkName="LowerLeg5")
        pyrosim.Send_Sensor_Neuron(name= '7', linkName="LowerLeg6")
        pyrosim.Send_Sensor_Neuron(name= '8', linkName="LowerLeg7")
        pyrosim.Send_Sensor_Neuron(name= '9', linkName="LowerLeg8")

        pyrosim.Send_Motor_Neuron(name= '10', jointName='Torso_Leg1')
        pyrosim.Send_Motor_Neuron(name= '11', jointName='Torso_Leg2')
        pyrosim.Send_Motor_Neuron(name= '12', jointName='Torso_Leg3')
        pyrosim.Send_Motor_Neuron(name= '13', jointName='Torso_Leg4')
        pyrosim.Send_Motor_Neuron(name= '14', jointName='Torso_Leg5')
        pyrosim.Send_Motor_Neuron(name= '15', jointName='Torso_Leg6')
        pyrosim.Send_Motor_Neuron(name= '16', jointName='Torso_Leg7')
        pyrosim.Send_Motor_Neuron(name= '17', jointName='Torso_Leg8')

        pyrosim.Send_Motor_Neuron(name= '18', jointName='Leg1_LowerLeg1')
        pyrosim.Send_Motor_Neuron(name= '19', jointName='Leg2_LowerLeg2')
        pyrosim.Send_Motor_Neuron(name= '20', jointName='Leg3_LowerLeg3')
        pyrosim.Send_Motor_Neuron(name= '21', jointName='Leg4_LowerLeg4')
        pyrosim.Send_Motor_Neuron(name= '22', jointName='Leg5_LowerLeg5')
        pyrosim.Send_Motor_Neuron(name= '23', jointName='Leg6_LowerLeg6')
        pyrosim.Send_Motor_Neuron(name= '24', jointName='Leg7_LowerLeg7')
        pyrosim.Send_Motor_Neuron(name= '25', jointName='Leg8_LowerLeg8')    

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