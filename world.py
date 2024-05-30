#So far, we have named our files using verbs, indicating what they do: generate.py a world and robot, simulate.py them, and then analyze.py them.
# We will now create one file for each class, and we will use a noun to name it.

#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

import pybullet as p

class WORLD:

    def __init__(self):
        self.planeId = p.loadURDF("plane.urdf")
        #self.boxId = p.loadURDF("cube.urdf")
        # Let's now simulate this box. This line tells pybullet to read in (import) the world described in box.sdf
        p.loadSDF("world.sdf")
        pass