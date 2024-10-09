import solution
import constants as c
import copy

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        self.parents = {}

        for parent_no in range(0,c.populationSize):
            # in the dictionary "parents", there is a key which is the int variable "parent"
            # that corresponds to an instance of the class "SOLUTION"
            # which is from the module "solution" imported from the top of the file. 
            # you need state "SOLUTION()" not "SOLUTION"
            # if you do the latter then you dont make instance but a direct reference which could chaneg the actual class
            self.parents[parent_no] = solution.SOLUTION()

        print(self.parents)
        

    def evolve(self):
        for parent_no in self.parents:
            self.parents[parent_no].Evaluate("GUI")
        # self.parent.Evaluate("GUI")
        # for currentGeneration in range(0,c.numberOfGenerations):
        #     self.Evolve_For_One_Generation()
        pass
            
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()
        #print(f"parent weights: {self.parent.weights}")
        #print(f"child weights: {self.child.weights}")

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child

    def Print(self):
        print(f"\nparent.fitness: {self.parent.fitness} child.fitness: {self.child.fitness}")
        
    def Show_Best(self):
       # self.parent.Evaluate("GUI")
        pass


