import math

import pybullet

import pyrosim.pyrosim as pyrosim

import pyrosim.constants as c

class NEURON: 

    def __init__(self,line):

        self.Determine_Name(line)

        self.Determine_Type(line)

        self.Search_For_Link_Name(line)

        self.Search_For_Joint_Name(line)

        self.Set_Value(0.0)

    def Add_To_Value( self, value ):

        self.Set_Value( self.Get_Value() + value )

    def Get_Joint_Name(self):

        return self.jointName

    def Get_Link_Name(self):

        return self.linkName

    def Get_Name(self):

        return self.name

    def Get_Value(self):

        return self.value

    def Is_Sensor_Neuron(self):

        return self.type == c.SENSOR_NEURON

    def Is_Hidden_Neuron(self):

        return self.type == c.HIDDEN_NEURON

    def Is_Motor_Neuron(self):

        return self.type == c.MOTOR_NEURON

    def Print(self):

        # self.Print_Name()

        # self.Print_Type()

        self.Print_Value()

        # print("")

    def Set_Value(self,value):

        self.value = value

    def Update_Sensor_Neuron(self):

        self.Set_Value(pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName))

    def Update_Hidden_Or_Motor_Neuron(self, neurons, synapses):
        self.Set_Value(0.0)
        #print(f'currently updating neuron: {self.Get_Name()}, its value is: {self.Get_Value()}')
        for synapse in synapses:
            # checks to see if the current synapse arrives at the neuron being updated.
            # does so by checking if the postsynaptic neuron "synapse[1]" (ie where the synapse is connecting to)
            # is equal to self.Get_Name() which returns the name of the neuron associated with the instance
            # of the neuron class that this funciton is in. This name is read from the nndf file when the class is initiated.
            if synapse[1] == self.Get_Name():
                #argument 1
                ## You have the key that references this synapse in the synapses dictionary. synapses[key] is an instance
                # of SYNAPSE; synapses[key].Get_Weight() will return the weight of the synapse.

                #argument 2
                ##The first element of the key's tuple is the presynaptic neuron's name. neurons[name] returns an instance
                # of NEURON. neurons[name].Get_Value() gets the current value of this neuron.
                self.Allow_Presynaptic_Neuron_To_Influence_Me(synapses[synapse].Get_Weight(), neurons[synapse[0]].Get_Value())
       # With enough incoming synapses, a neuron may thus take on very positive or very negative numbers. Let us thus
        # threshold the value of each neuron using an activation function to the range [-1,1].
        self.Threshold()
        #print(f'finished updating neuron: {self.Get_Name()}, its value is: {self.Get_Value()}')

    def Allow_Presynaptic_Neuron_To_Influence_Me(self, synapse_weight, presynaptic_neuron_value):
        print(synapse_weight, presynaptic_neuron_value)
        product = synapse_weight * presynaptic_neuron_value
        #the argument to this function is added to the neuron. this funciton exisits within an instance of the neuron class. each instance of the class is a neuron in the neual net.
        self.Add_To_Value(product)

# -------------------------- Private methods -------------------------

    def Determine_Name(self,line):

        if "name" in line:

            splitLine = line.split('"')

            self.name = splitLine[1]

    def Determine_Type(self,line):

        if "sensor" in line:

            self.type = c.SENSOR_NEURON

        elif "motor" in line:

            self.type = c.MOTOR_NEURON

        else:

            self.type = c.HIDDEN_NEURON

    def Print_Name(self):

       print(self.name)

    def Print_Type(self):

       print(self.type)

    def Print_Value(self):

       print(self.value , " " , end="" )

    def Search_For_Joint_Name(self,line):

        if "jointName" in line:

            splitLine = line.split('"')

            self.jointName = splitLine[5]

    def Search_For_Link_Name(self,line):

        if "linkName" in line:

            splitLine = line.split('"')

            self.linkName = splitLine[5]

    def Threshold(self):

        self.value = math.tanh(self.value)
