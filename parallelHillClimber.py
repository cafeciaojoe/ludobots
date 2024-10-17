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
        self.Print()
        self.Select()

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
            solutions[i].Start_Simulation("DIRECT")

        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()

    def Select(self):
        for i in self.parents:
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]

    def Print(self):
        print("\n")
        for i in self.parents:
            print(f"\nparent{str(i)}.fitness: {self.parents[i].fitness} child{str(i)}.fitness: {self.children[i].fitness}")
        print("\n")
        
    def Show_Best(self):
        # initialise this variable as infinite to avoid anything being higer than it on the first pass
        best_fitness = float('inf')
        # initialise as None, we can check later if there is actually a better fitness
        best_i = None

        # Handle edge cases where self.parents might be empty
        if not self.parents:
            print("self.parents is empty!")
            return

        #a ccessing dictionary items directly can be more efficient. 
        # When you use "for i in self.parents" (like you have been in this tutorial), you need to access 
        # the value with self.parents[i] inside the loop, which involves an additional dictionary lookup. 
        # Using "for i, parent in self.parents.items()"" avoids this extra lookup.
        for i, parent in self.parents.items():
            current_fitness = parent.fitness
            if current_fitness < best_fitness:
                best_fitness = current_fitness
                best_i = i

        if best_i is not None:
            self.parents[best_i].Start_Simulation("GUI")
            print("\n")
            print(f"Best Fitness: {self.parents[best_i].fitness}")
            print("\n")



