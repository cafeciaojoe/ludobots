import os
import hillclimber

#create an instance of HILL_CLIMBER class called hc
hc = hillclimber.HILL_CLIMBER()
hc.evolve()
hc.Show_Best()

# for i in range(0,5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")

