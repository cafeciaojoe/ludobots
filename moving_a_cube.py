import numpy as np
import pybullet as p
import pybullet_data
import time

# Motion parameters
base_z_height = 1.0  # starting height in meters
z_step = 0.01  # 1cm steps
total_steps = 500  # 250 up + 250 down
sample_rate = 100  # Hz

# Generate positions (only Z changes, X and Y stay at 0)
positions = np.zeros((total_steps, 3))
z_positions = np.zeros(total_steps)
z_positions[:250] = base_z_height + np.arange(250) * z_step  # Up
z_positions[250:] = (base_z_height + 2.49) - np.arange(250) * z_step  # Down
positions[:, 2] = z_positions  # Set Z positions

# Initialize PyBullet
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, 0)
p.loadURDF("plane.urdf")

# Create cube
cube_size = 0.1
visualShapeId = p.createVisualShape(
    shapeType=p.GEOM_BOX,
    halfExtents=[cube_size/2]*3
)
cubeId = p.createMultiBody(
    baseMass=1,
    baseVisualShapeIndex=visualShapeId,
    basePosition=[0, 0, 0]
)

# Main loop
time_step = 1/sample_rate
for position in positions:
    start_time = time.time()

    p.resetBasePositionAndOrientation(
        cubeId,
        position,
        [0, 0, 0, 1]
    )

    p.stepSimulation()

    elapsed = time.time() - start_time
    if elapsed < time_step:
        time.sleep(time_step - elapsed)

p.disconnect()
