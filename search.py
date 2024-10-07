import os
import parallelHillClimber

#create an instance of HILL_CLIMBER class called hc
phc = parallelHillClimber.PARALLEL_HILL_CLIMBER()
phc.evolve()
phc.Show_Best()

# for i in range(0,5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")

