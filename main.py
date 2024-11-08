# main.py
from simulation_drone_bridge import SimulationDroneBridge

if __name__ == '__main__':
    try:
        bridge = SimulationDroneBridge()
        bridge.run()
    except KeyboardInterrupt:
        print("Shutting down...")
        bridge.running = False
