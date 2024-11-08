# test_sim.py
from simulation_gpt import SIMULATION

def test_callback(positions):
    print(f"Received positions: {positions}")

sim = SIMULATION("GUI", position_callback=test_callback)
sim.Run()
