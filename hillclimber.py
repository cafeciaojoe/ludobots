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
            pass

    def Evolve_For_One_Generation():
        self.Spawn()
        self.Mutate()
        self.child.Evaluate()
        self.Select()

    def Spawn():
        self.child = copy.deepcopy(self.parent)
        
        pass

    def Mutate():
        pass

    def Select():
        pass



