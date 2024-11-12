#So far, we have named our files using verbs, indicating what they do: generate.py a world and robot, simulate.py them, and then analyze.py them.
# We will now create one file for each class, and we will use a noun to name it.

import logging

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

import usb_config  # This will set up the backend (from chatgpt) 

from world import WORLD
from robot import ROBOT

import pybullet as p
import numpy
import time
import pyrosim.pyrosim as pyrosim
#plane.urdf comes with pybullet; you do not have to generate it. We have to tell pybullet where to find it by adding
import pybullet_data
import os
import math
import random
import constants as c


#Note: We are going to name all of our classes in ALL CAPS to distinguish them from file names and variable names.

class SIMULATION:

    def __init__(self, directOrGUI):

        self.uri = uri_helper.uri_from_env(default='radio://0/90/2M/A0A0A0A0AA')
        self.uri_2 = uri_helper.uri_from_env(default='radio://0/80/2M/A0A0A0A0A8')
        self.uri_3 = uri_helper.uri_from_env(default='radio://0/80/2M/A0A0A0A0AC')

        cflib.crtp.init_drivers()

        self.flight_time = 1

        self.positions = {}

        self.directOrGUI = directOrGUI

        if directOrGUI == "DIRECT":
            # running the sim "blind"
            self.physicsClient = p.connect(p.DIRECT)
        else:
            # running the sim "heads up"
            self.physicsClient = p.connect(p.GUI)

        # this line allows the use of an existing asset, ie a floor e.g. plane.udrf
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # to disable the sidebars on the pybullet simulation.
        # This change will also dramatically speed up the GUI simulation on some platforms.
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

        # ou will have noticed that if you manipulate the cube and then let it go, it will float away.
        # This is because no forces are currently at work in your simulated world.
        p.setGravity(c.Xgravity, c.Ygravity, c.Zgravity)

        self.world = WORLD()
        self.robot = ROBOT()

        # Pyrosim has to do some additional setting up when it is used to simulate sensors. So, add just before entering the for loop in simulate.py.
        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()

        # print("sleep")
        # time.sleep(5)
        
        # exit()

    def Run(self):
        loops = c.loops
        for t in range(0, loops):
            #print(i)
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.think()
            self.robot.Act(t)

            self.positions = self.robot.Get_Positions()
            print("B",self.positions["BackLeg"][0]/5,  self.positions["BackLeg"][1]/5,  self.positions["BackLeg"][2]/5)
            print("T",self.positions["Torso"][0]/5,  self.positions["Torso"][1]/5,  self.positions["Torso"][2]/5)
            print("F",self.positions["FrontLeg"][0]/5,  self.positions["FrontLeg"][1]/5,  self.positions["FrontLeg"][2]/5)

            if self.directOrGUI == "GUI":
                time.sleep(c.loopSleep)

            keys = p.getKeyboardEvents()
            cam = p.getDebugVisualizerCamera()
            #Keys to change camera
            if keys.get(108):  #L (right)
                xyz = cam[11]
                x= float(xyz[0]) + 0.125
                y = xyz[1]
                z = xyz[2]
                p.resetDebugVisualizerCamera(cameraYaw = cam[8], cameraPitch= cam[9],cameraDistance = cam[10],cameraTargetPosition=[x,y,z])
            if keys.get(106):  #J (left)
                xyz = cam[11]
                x= float(xyz[0]) - 0.125
                y = xyz[1]
                z = xyz[2]
                p.resetDebugVisualizerCamera(cameraYaw = cam[8], cameraPitch= cam[9],cameraDistance = cam[10],cameraTargetPosition=[x,y,z])
            if keys.get(105):  #I (up)
                xyz = cam[11]
                x = xyz[0] 
                y = float(xyz[1]) + 0.125
                z = xyz[2]
                p.resetDebugVisualizerCamera(cameraYaw = cam[8], cameraPitch= cam[9],cameraDistance = cam[10],cameraTargetPosition=[x,y,z])
            if keys.get(107):  #K (down)
                xyz = cam[11]
                x = xyz[0] 
                y = float(xyz[1]) - 0.125
                z = xyz[2]
                p.resetDebugVisualizerCamera(cameraYaw = cam[8], cameraPitch= cam[9],cameraDistance = cam[10],cameraTargetPosition=[x,y,z]) 


    def RunFly(self):
        loops = c.loops
        keys = p.getKeyboardEvents()
        cam = p.getDebugVisualizerCamera()

        with SyncCrazyflie(self.uri, cf=Crazyflie(rw_cache='./cache')) as scf_1:
            with SyncCrazyflie(self.uri_2, cf=Crazyflie(rw_cache='./cache')) as scf_2:
                with SyncCrazyflie(self.uri_3, cf=Crazyflie(rw_cache='./cache')) as scf_3:

                    commander_0 = scf_1.cf.high_level_commander
                    commander_1 = scf_2.cf.high_level_commander
                    commander_2 = scf_3.cf.high_level_commander

                    commander_0.takeoff(.3, 2.0)
                    commander_1.takeoff(.4, 2.0)
                    commander_2.takeoff(.3, 2.0)

                    time.sleep(5)

                    for t in range(0, loops):
                        #print(i)
                        p.stepSimulation()
                        self.robot.Sense(t)
                        self.robot.think()
                        self.robot.Act(t)
                        # Usage (assuming you have already loaded the robot):
                        # robotId = p.loadURDF("body.urdf")
                        self.positions = self.robot.Get_Positions()

                        # note: xy switched
                        commander_0.go_to(self.positions["Torso"][1]/5,  self.positions["Torso"][0]/5,  self.positions["Torso"][2]/5, 0, c.loopSleep, relative=False)
                        commander_1.go_to(self.positions["BackLeg"][1]/5,  self.positions["BackLeg"][0]/5,  self.positions["BackLeg"][2]/5, 0, c.loopSleep, relative=False)
                        commander_2.go_to(self.positions["FrontLeg"][1]/5,  self.positions["FrontLeg"][0]/5,  self.positions["FrontLeg"][2]/5, 0, c.loopSleep, relative=False)
                        
                        if self.directOrGUI == "GUI":
                            time.sleep(c.loopSleep)

                        #Keys to change camera
                        if keys.get(108):  #L (right)
                            xyz = cam[11]
                            x= float(xyz[0]) + 0.125
                            y = xyz[1]
                            z = xyz[2]
                            p.resetDebugVisualizerCamera(cameraYaw = cam[8], cameraPitch= cam[9],cameraDistance = cam[10],cameraTargetPosition=[x,y,z])
                        if keys.get(106):  #J (left)
                            xyz = cam[11]
                            x= float(xyz[0]) - 0.125
                            y = xyz[1]
                            z = xyz[2]
                            p.resetDebugVisualizerCamera(cameraYaw = cam[8], cameraPitch= cam[9],cameraDistance = cam[10],cameraTargetPosition=[x,y,z])
                        if keys.get(105):  #I (up)
                            xyz = cam[11]
                            x = xyz[0] 
                            y = float(xyz[1]) + 0.125
                            z = xyz[2]
                            p.resetDebugVisualizerCamera(cameraYaw = cam[8], cameraPitch= cam[9],cameraDistance = cam[10],cameraTargetPosition=[x,y,z])
                        if keys.get(107):  #K (down)
                            xyz = cam[11]
                            x = xyz[0] 
                            y = float(xyz[1]) - 0.125
                            z = xyz[2]
                            p.resetDebugVisualizerCamera(cameraYaw = cam[8], cameraPitch= cam[9],cameraDistance = cam[10],cameraTargetPosition=[x,y,z]) 

                time.sleep(3)
                
                commander_0.land(0.0, 2.0)
                commander_1.land(0.0, 2.0)
                commander_2.land(0.0, 2.0)

                time.sleep(3)

                commander_0.stop()
                commander_1.stop()
                commander_2.stop()

def Get_Fitness(self):
    self.robot.Get_Fitness()
    pass

    #https://www.geeksforgeeks.org/destructors-in-python/
def __del__(self):
        #self.robot.Save_Values()
        p.disconnect()

if __name__ == '__main__':
    directOrGUI = 'GUI'
    simulation = SIMULATION(directOrGUI)
    simulation.Run()    
    #simulation.RunFly()