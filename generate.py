"""what is in the world"""

"""This file will use pyrosim to generate a link (later, several links comprising the world),
store it in a special file called world.sdf, and
simulate.py will then read it in and simulate it.
"""

import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1


def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-3, -3, height/2], size=[length, width, height])
    pyrosim.End()

def Create_TARS():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Link0", pos=[0, 0, .5], size=[length, width, height])
    #Joints with no upstream joint have absolute positions. Every other joint has a position relative to its upstream joint.
    #https://docs.google.com/presentation/d/1zvZzFyTf8PBNjzQZx_gZk84aUntZo2bUKhpe78yT4OY/edit#slide=id.g10dad2fba23_2_371
    pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[0, 0, 1])
    pyrosim.Send_Cube(name="Link1", pos=[0, 0, .5], size=[length, width, height])
    pyrosim.Send_Joint(name="Link1_Link2", parent="Link1", child="Link2", type="revolute", position=[0, 0, 1])
    pyrosim.Send_Cube(name="Link2", pos=[0, 0, .5], size=[length, width, height])
    pyrosim.Send_Joint(name="Link2_Link3", parent="Link2", child="Link3", type="revolute", position=[0, .5, .5])
    pyrosim.Send_Cube(name="Link3", pos=[0, .5, 0], size=[length, width, height])
    pyrosim.Send_Joint(name="Link3_Link4", parent="Link3", child="Link4", type="revolute", position=[0, 1, 0])
    pyrosim.Send_Cube(name="Link4", pos=[0, .5, 0], size=[length, width, height])
    pyrosim.Send_Joint(name="Link4_Link5", parent="Link4", child="Link5", type="revolute", position=[0, .5, -.5])
    pyrosim.Send_Cube(name="Link5", pos=[0, 0, -.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Link5_Link6", parent="Link5", child="Link6", type="revolute", position=[0, 0, -1])
    pyrosim.Send_Cube(name="Link6", pos=[0, 0, -.5], size=[length, width, height])

    pyrosim.End()


def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="BackLeg", pos=[.5, 0, .5], size=[length, width, height])
    # Joints with no upstream joint have absolute positions. Every other joint has a position relative to its upstream joint.
    # https://docs.google.com/presentation/d/1zvZzFyTf8PBNjzQZx_gZk84aUntZo2bUKhpe78yT4OY/edit#slide=id.g10dad2fba23_2_371
    pyrosim.Send_Joint(name="BackLeg_Torso", parent="BackLeg", child="Torso", type="revolute", position=[1, 0, 1])
    pyrosim.Send_Cube(name="Torso", pos=[.5, 0, .5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[1, 0, 0])
    pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5], size=[length, width, height])

    pyrosim.End()

Create_World()
Create_Robot()