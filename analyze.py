import numpy
import os
import matplotlib.pyplot

backLegSensorValues = numpy.load(os.path.join('data','backLegSensorValues.npy'))
frontLegSensorValues = numpy.load(os.path.join('data','frontLegSensorValues.npy'))

matplotlib.pyplot.plot(backLegSensorValues,label='backLeg')
matplotlib.pyplot.plot(frontLegSensorValues,label='frontLeg')

matplotlib.pyplot.legend()
matplotlib.pyplot.show()

