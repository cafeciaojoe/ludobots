"""How the world is simulated"""

import pybullet as p
import numpy
import time
import pyrosim.pyrosim as pyrosim
#plane.urdf comes with pybullet; you do not have to generate it. We have to tell pybullet where to find it by adding
import pybullet_data
import os

physicsClient = p.connect(p.GUI)
#this line allows the use of an existing asset, ie a floor e.g. plane.udrf
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# to disable the sidebars on the pybullet simulation.
# This change will also dramatically speed up the GUI simulation on some platforms.
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

#ou will have noticed that if you manipulate the cube and then let it go, it will float away.
# This is because no forces are currently at work in your simulated world.
p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

#Let's now simulate this box. This line tells pybullet to read in (import) the world described in box.sdf
p.loadSDF("world.sdf")

#Pyrosim has to do some additional setting up when it is used to simulate sensors. So, add just before entering the for loop in simulate.py.
pyrosim.Prepare_To_Simulate(robotId)

loops = 10000

frontLegSensorValues = numpy.zeros(loops)
backLegSensorValues = numpy.zeros(loops)

for i in range(1,loops):
    p.stepSimulation()
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    print(backLegSensorValues[i],frontLegSensorValues[i])
    time.sleep(.0016)

#https://stackoverflow.com/questions/43731481/how-to-use-np-save-to-save-files-in-different-directory-in-python
numpy.save(os.path.join('data','frontLegSensorValues'),frontLegSensorValues)
numpy.save(os.path.join('data','backLegSensorValues'),backLegSensorValues)


p.disconnect()