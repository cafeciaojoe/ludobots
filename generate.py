import pyrosim.pyrosim as pyrosim

#this adds a world called box.
pyrosim.Start_SDF("box.sdf")

#this adds a box called box in the world called box.
pyrosim.Send_Cube(name="Box", pos=[0,0,0.5] , size=[1,1,1])

pyrosim.End()