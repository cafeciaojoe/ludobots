import sys

"""How the world is simulated"""

from simulation import SIMULATION

#This code checks if the argument is provided and if it is either "GUI" or "DIRECT". 
# If not, it prints a usage message and exits the program.
# NOTE this was not part of the tutorial so delete if causing issues. 
if len(sys.argv) < 2 or sys.argv[1] not in ["GUI", "DIRECT"]:
    print("Usage: python simulate.py [GUI|DIRECT]")
    sys.exit(1)

# https://stackoverflow.com/questions/4117530/what-does-sys-argv1-mean-what-is-sys-argv-and-where-does-it-come-from
# returns the first argument when running the script in the terminal.
directOrGUI = sys.argv[1]

simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()


