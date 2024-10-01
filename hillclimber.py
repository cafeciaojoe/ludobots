import solution
import constants as c
import copy

class HILL_CLIMBER:

    def __init__(self):
        self.parent = solution.SOLUTION()
        pass

    def evolve(self):
        self.parent.Evaluate()
        for currentGeneration in range(0,c.numberOfGenerations):
            self.Evolve_For_One_Generation()
            

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()
        print(f"parent weights: {self.parent.weights}")
        print(f"child weights: {self.child.weights}")
        exit()

    def Select(self):
        pass



