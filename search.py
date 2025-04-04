import os
import parallelHillClimber
import last_best_replay

# last_best_replay.replay_simulation() 
# exit()

phc = parallelHillClimber.PARALLEL_HILL_CLIMBER()
phc.evolve()
phc.Show_Best()

