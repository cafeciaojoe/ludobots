#There are many numbers being assigned to variables in simulate.py.
# We want to put all these values in the same place, so we can easily modify them later.

import math

Xgravity = 0
Ygravity = 0
Zgravity = -9.8

loops = 1000
loopSleep = .001

amplitude = math.pi/4
frequency = 10
offset = 0
#not needed maybe?
TargetAngleMin = 0
TargetAngleMax = 2*math.pi

amplitudeFrontLeg = math.pi/4
frequencyFrontLeg = 10
phaseOffsetFrontLeg = 0

amplitudeBackLeg = math.pi/4
frequencyBackLeg = 10
phaseOffsetBackLeg = math.pi/4

frontLegTargetAngleMin = 0
frontLegTargetAngleMax = 2*math.pi

backLegTargetAngleMin = 0
backLegTargetAngleMax = 2*math.pi

frontLegForceMax = 50
backLegForceMax = 50

numberOfGenerations = 10

