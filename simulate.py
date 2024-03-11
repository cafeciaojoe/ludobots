import pybullet as p
import time

physicsClient = p.connect(p.GUI)

# to disable the sidebars on the pybullet simulation.
# This change will also dramatically speed up the GUI simulation on some platforms.
#p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

# Let's slow things down so we can see our simulated world.
# Between the connect and disconnect lines, include a for loop that iterates 1000 times.
# Inside the loop include
for i in range(1,1000):
    p.stepSimulation()
    time.sleep(.016)
    print(i)

p.disconnect()