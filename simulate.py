"""How the world is simulated"""

from simulation import SIMULATION

simulation = SIMULATION()
simulation.run()

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


# loops = c.loops
#
# amplitudeFrontLeg = c.amplitudeFrontLeg
# frequencyFrontLeg = c.frequencyFrontLeg
# phaseOffsetFrontLeg = c.phaseOffsetFrontLeg
#
# amplitudeBackLeg = c.amplitudeBackLeg
# frequencyBackLeg = c.frequencyBackLeg
# phaseOffsetBackLeg = c.phaseOffsetBackLeg
#
# # simple sine wave driven synchronised movement
# #targetAngles = .8 * numpy.sin(numpy.linspace(0, 2*math.pi, num=loops, endpoint=True))
#
# frontLegTargetAngles = amplitudeFrontLeg * numpy.sin(frequencyFrontLeg * numpy.linspace(c.frontLegTargetAngleMin, c.frontLegTargetAngleMax, num=loops, endpoint=True) + phaseOffsetFrontLeg)
# backLegTargetAngles = amplitudeBackLeg * numpy.sin(frequencyBackLeg * numpy.linspace(c.backLegTargetAngleMin, c.backLegTargetAngleMax, num=loops, endpoint=True) + phaseOffsetBackLeg)
#
# numpy.save(os.path.join('data','frontLegTargetAngles'), frontLegTargetAngles)
# numpy.save(os.path.join('data','backLegTargetAngles'), backLegTargetAngles)
#
#
# #https://stackoverflow.com/questions/43731481/how-to-use-np-save-to-save-files-in-different-directory-in-python
# numpy.save(os.path.join('data','frontLegSensorValues'),frontLegSensorValues)
# numpy.save(os.path.join('data','backLegSensorValues'),backLegSensorValues)





