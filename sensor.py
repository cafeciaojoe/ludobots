#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import numpy

class SENSOR:

    def __init__(self, linkname):
        self.linkName = linkname
        self.values = numpy.zeros(100)
        pass