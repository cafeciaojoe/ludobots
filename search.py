import os
import parallelHillClimber
import time

#phc = parallelHillClimber.PARALLEL_HILL_CLIMBER()
#phc.evolve()
#phc.Show_Best()

for i in range(0,12):
    phc = parallelHillClimber.PARALLEL_HILL_CLIMBER()
    phc.evolve()
    phc.Show_Best()
    time.sleep(10)
