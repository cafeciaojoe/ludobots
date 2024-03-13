"""what is in the world"""

"""This file will use pyrosim to generate a link (later, several links comprising the world),
store it in a special file called world.sdf, and
simulate.py will then read it in and simulate it.
"""

import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x_pos = 0
y_pos = 0
z_pos = .5



# to tell pyrosim the name of the file where information about the world you're about to create
# should be stored. This world will currently be called box, because it will only contain a box
# (links can be spheres, cylinders, or boxes).
pyrosim.Start_SDF("box.sdf")

# stores a box with initial position , and length, width and height, in box.sdf.
#pyrosim.Send_Cube(name="Box", pos=[0,0,.5] , size=[length,width,height])
#pyrosim.Send_Cube(name="Box2", pos=[1,0,1.5] , size=[length,width,height])

#making a tower
for i in range(0,3):
    for j in range(0,3):
        for k in range(0,3):
            pyrosim.Send_Cube(name="Box", pos=[k, j, (i + height/2)], size=[length, width, height])
    length *= .9
    width *= .9
    height *= .9


pyrosim.End()