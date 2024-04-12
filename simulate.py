"""How the world is simulated"""

# from simulation import SIMULATION

# simulation = SIMULATION()



import pybullet as p
import numpy
import time
import pyrosim.pyrosim as pyrosim
#plane.urdf comes with pybullet; you do not have to generate it. We have to tell pybullet where to find it by adding
import pybullet_data
import os
import math
import random
import constraints as c

physicsClient = p.connect(p.GUI)
#this line allows the use of an existing asset, ie a floor e.g. plane.udrf
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# to disable the sidebars on the pybullet simulation.
# This change will also dramatically speed up the GUI simulation on some platforms.
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

#ou will have noticed that if you manipulate the cube and then let it go, it will float away.
# This is because no forces are currently at work in your simulated world.
p.setGravity(c.Xgravity,c.Ygravity, c.Zgravity)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

#Let's now simulate this box. This line tells pybullet to read in (import) the world described in box.sdf
p.loadSDF("world.sdf")

#Pyrosim has to do some additional setting up when it is used to simulate sensors. So, add just before entering the for loop in simulate.py.
pyrosim.Prepare_To_Simulate(robotId)

loops = c.loops

frontLegSensorValues = numpy.zeros(loops)
backLegSensorValues = numpy.zeros(loops)

amplitudeFrontLeg = c.amplitudeFrontLeg
frequencyFrontLeg = c.frequencyFrontLeg
phaseOffsetFrontLeg = c.phaseOffsetFrontLeg

amplitudeBackLeg = c.amplitudeBackLeg
frequencyBackLeg = c.frequencyBackLeg
phaseOffsetBackLeg = c.phaseOffsetBackLeg

# simple sine wave driven synchronised movement
#targetAngles = .8 * numpy.sin(numpy.linspace(0, 2*math.pi, num=loops, endpoint=True))

frontLegTargetAngles = amplitudeFrontLeg * numpy.sin(frequencyFrontLeg * numpy.linspace(c.frontLegTargetAngleMin, c.frontLegTargetAngleMax, num=loops, endpoint=True) + phaseOffsetFrontLeg)
backLegTargetAngles = amplitudeBackLeg * numpy.sin(frequencyBackLeg * numpy.linspace(c.backLegTargetAngleMin, c.backLegTargetAngleMax, num=loops, endpoint=True) + phaseOffsetBackLeg)

numpy.save(os.path.join('data','frontLegTargetAngles'), frontLegTargetAngles)
numpy.save(os.path.join('data','backLegTargetAngles'), backLegTargetAngles)


for i in range(1,loops):
    p.stepSimulation()
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    #print(backLegSensorValues[i],frontLegSensorValues[i])

    #During each step of the simulation, we are going to simulate a motor that supplies force to one of the robot's joints. To do so, add this statement
    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName="Torso_FrontLeg",

        controlMode=p.POSITION_CONTROL,

        #the desired angle between the two links connected by the joint
        targetPosition= frontLegTargetAngles[i],

        maxForce=c.frontLegForceMax)

    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName="Torso_BackLeg",

        controlMode=p.POSITION_CONTROL,

        #the desired angle between the two links connected by the joint
        targetPosition= backLegTargetAngles[i],

        maxForce=c.frontLegForceMax)

    time.sleep(c.loopSleep)

#https://stackoverflow.com/questions/43731481/how-to-use-np-save-to-save-files-in-different-directory-in-python
numpy.save(os.path.join('data','frontLegSensorValues'),frontLegSensorValues)
numpy.save(os.path.join('data','backLegSensorValues'),backLegSensorValues)


p.disconnect()

