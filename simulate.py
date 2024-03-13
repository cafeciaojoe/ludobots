"""How the world is simulated"""

import pybullet as p
import time
#plane.urdf comes with pybullet; you do not have to generate it. We have to tell pybullet where to find it by adding
import pybullet_data

physicsClient = p.connect(p.GUI)
#this line allows the use of an existing asset, ie a floor e.g. plane.udrf
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# to disable the sidebars on the pybullet simulation.
# This change will also dramatically speed up the GUI simulation on some platforms.
#p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

#ou will have noticed that if you manipulate the cube and then let it go, it will float away.
# This is because no forces are currently at work in your simulated world.
p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")

#Let's now simulate this box. This line tells pybullet to read in (import) the world described in box.sdf
p.loadSDF("box.sdf")

# Let's slow things down so we can see our simulated world.
# Between the connect and disconnect lines, include a for loop that iterates 1000 times.
# Inside the loop include
for i in range(1,1000):
    p.stepSimulation()
    time.sleep(.000016)
    print(i)

p.disconnect()