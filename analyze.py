import numpy
import os
import matplotlib.pyplot

backLegSensorValues = numpy.load(os.path.join('data','backLegSensorValues.npy'))
frontLegSensorValues = numpy.load(os.path.join('data','frontLegSensorValues.npy'))

targetAngles = numpy.load(os.path.join('data','targetAngles.npy'))

#matplotlib.pyplot.plot(backLegSensorValues,label='backLeg', linewidth=2)
#matplotlib.pyplot.plot(frontLegSensorValues,label='frontLeg',linewidth=1)

matplotlib.pyplot.plot(targetAngles,label='targetAngles',linewidth=1)

matplotlib.pyplot.legend()
matplotlib.pyplot.show()

