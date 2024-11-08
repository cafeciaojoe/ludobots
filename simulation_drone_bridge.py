# simulation_drone_bridge.py
from queue import Queue
from threading import Thread
import time
import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from simulation_gpt import SIMULATION  # Your existing simulation file

import usb_config  # This will set up the backend (from chatgpt) 

class SimulationDroneBridge:
    def __init__(self):
        self.position_queue = Queue()
        self.running = True

    def position_callback(self, positions):
        """Callback function to receive positions from simulation"""
        self.position_queue.put(positions)

    def convert_sim_to_drone_coords(self, position):
        """Convert simulation coordinates to drone coordinates"""
        # Adjust these conversions based on your coordinate systems
        x = position.get('x', 0)
        y = position.get('y', 0)
        z = position.get('z', 0)

        # Add scaling if needed
        scale = .5
        return x * scale, y * scale, z * scale

    def run_drone_sequence(self, scf):
        """Control sequence for each drone"""
        commander = scf.cf.high_level_commander

        # Take off
        commander.takeoff(1.0, 2.0)
        time.sleep(3)

        # Main control loop
        while self.running:
            try:
                position = self.position_queue.get(timeout=1.0)
                x, y, z = self.convert_sim_to_drone_coords(position)
                commander.go_to(x, y, z, 0, 0.1, relative=False)
                time.sleep(0.1)
            except Queue.Empty:
                continue
            except Exception as e:
                print(f"Error in drone control: {e}")
                break

        # Land when done
        commander.land(0.0, 2.0)
        time.sleep(2)
        commander.stop()

    def run(self):
        # Initialize simulation
        sim = SIMULATION("GUI", position_callback=self.position_callback)
        sim_thread = Thread(target=sim.Run)

        # Initialize drone communication
        cflib.crtp.init_drivers()
        factory = CachedCfFactory(rw_cache='./cache')

        # # Your drone URIs
        # uris = {
        #     'radio://0/90/2M/A0A0A0A0AA',
        #     'radio://0/80/2M/A0A0A0A0A8',
        #     'radio://0/80/2M/A0A0A0A0AC',
        # }

                # Your drone URIs
        uris = {
            'radio://0/90/2M/A0A0A0A0AA'
        }

        # Start simulation thread
        sim_thread.start()

        # Start drone control
        with Swarm(uris, factory=factory) as swarm:
            swarm.reset_estimators()
            swarm.parallel_safe(self.run_drone_sequence)
