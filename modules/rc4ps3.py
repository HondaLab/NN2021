#!/usr/bin/python3

# rc4ps3.py
# Control left and right motors by single jyostick
# Yasushi Honda 2021 9/3

# How to execute
# sudo pigpiod
# pyhton3 rcXY.py 

import modules.keyin as keyin # キーボード入力を監視するモジュール
import modules.motor as mt # pwmでモーターを回転させるためのモジュール
import numpy as np
import time

class Assign():

   def __init__(self):
      self.mL=mt.Lmotor(23)
      self.mR=mt.Rmotor(14)
      self.csv=mt.Servo(18)
      self.left=0
      self.right=0
      self.angl=0

   def update(self,Rx,Ry,dL,dR):

      # Controll by PS3 controller
      self.left=-70*Ry+50*Rx
      self.right=-70*Ry-50*Rx

      if dL<1000 or dR<1000:
         if np.abs(dL-dR)>50:
            self.angl+=0.0005*(dR-dL)
            if self.angl>120: self.angl=120
            if self.angl<-120: self.angl=-120
      else:
         self.angl=0.0

      self.angl=0.0
      Run(self.mL,self.mR,self.csv,self.left,self.right,self.angl)
      #print("\r %4d %4d %4d" % (self.left,self.right,self.angl),end='')

      return self.left, self.right, self.angl

   def stop(self):
      self.mL.run(0)
      self.mR.run(0)
      self.csv.move(0)

def Run(mL,mR,sv,left,right,angl):
   if left<-100: left = -100
   if left>100: left = 100
   mL.run(left)
   if right<-100: right = -100
   if right>100: right = 100
   mR.run(right)
   if angl>120: angl=120
   if angl<-120: angl=-120
   sv.move(angl)

