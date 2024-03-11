import pybullet as p
import time

physicsClient = p.connect(p.GUI)

# Let's slow things down so we can see our simulated world.
# Between the connect and disconnect lines, include a for loop that iterates 1000 times.
# Inside the loop include
for i in range(1,100000):
    p.stepSimulation()

p.disconnect()