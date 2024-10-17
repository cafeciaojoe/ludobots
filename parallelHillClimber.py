import solution
import constants as c
import copy

import os

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")

        self.parents = {}

        self.nextAvailableID = 0 

        for i in range(0,c.populationSize):
            # in the dictionary "parents", there is a key which is the int variable "parent"
            # that corresponds to an instance of the class "SOLUTION"
            # which is from the module "solution" imported from the top of the file. 
            # you need state "SOLUTION()" not "SOLUTION"
            # if you do the latter then you dont make instance but a direct reference which could chaneg the actual class
            self.parents[i] = solution.SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1 

    def evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(0,c.numberOfGenerations):
            self.Evolve_For_One_Generation()
        pass
            
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        exit()
        # self.Print()
        # self.Select()

    def Spawn(self):
        self.children = {}
        for i in self.parents:
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].setID(self.nextAvailableID)
            self.nextAvailableID += 1 

    def Mutate(self):
        for i in self.children:
            self.children[i].Mutate()
        #print(f"parent weights: {self.parent.weights}")
        #print(f"child weights: {self.child.weights}")

    def Evaluate(self,solutions):
        for i in solutions:
            solutions[i].Start_Simulation("GUI")

        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child

    def Print(self):
        print(f"\nparent.fitness: {self.parent.fitness} child.fitness: {self.child.fitness}")
        
    def Show_Best(self):
       # self.parent.Evaluate("GUI")
        pass


