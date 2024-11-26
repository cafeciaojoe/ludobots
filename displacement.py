import pybullet as p
import pybullet_data
import time
import numpy as np

# Initialize PyBullet
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Load plane and cube
planeId = p.loadURDF("plane.urdf")
startPos = [0, 0, 1]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])
boxId = p.loadURDF("cube.urdf", startPos, startOrientation)

# Store initial position
initial_pos = np.array(p.getBasePositionAndOrientation(boxId)[0])

print(initial_pos)

def get_displacement():
    # Get current position
    current_pos = np.array(p.getBasePositionAndOrientation(boxId)[0])

    # Calculate displacement vector
    displacement_vector = current_pos - initial_pos

    # Calculate magnitude of displacement
    displacement_magnitude = np.linalg.norm(displacement_vector)

    return displacement_vector, displacement_magnitude

# Simulation loop
for i in range(1000):
    p.stepSimulation()

    # Apply a force to move the cube (optional)
    if i < 100:
        p.applyExternalForce(boxId, -1, [10, 0, 0], [0, 0, 0], p.WORLD_FRAME)

    # Get displacement every 100 steps
    if i % 100 == 0:
        disp_vector, disp_magnitude = get_displacement()
        print(f"Displacement vector: {disp_vector}")
        print(f"Displacement magnitude: {disp_magnitude:.2f} meters")

    time.sleep(1./240.)

p.disconnect()
