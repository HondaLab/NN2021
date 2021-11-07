#!/usr/bin/python3

# rc3b.py
# Yasushi Honda 2021 9/3

# How to execute
# sudo pigpiod
# pyhton3 rcXY.py 

import modules.keyin as keyin # キーボード入力を監視するモジュール
import modules.motor5a as mt # pwmでモーターを回転させるためのモジュール
import modules.motor1 as sv # カメラサーボ
import time


STEP=8
HANDLE_STEP=8
HANDLE_TIME=0.3
TRIM_STEP=8
TRIM_TIME=0.2
ANGL_GAIN=0.6

class KeyAssign():

   def __init__(self):
      self.mL=mt.Lmotor(17)
      self.mR=mt.Rmotor(18)
      self.csv=sv.Rmotor(27)
      self.left=0
      self.right=0

   def update(self,ch):
      if ch == "j" :
         #TRIM_STEP=int(0.5*(left+right)*1.0)
         self.left-= TRIM_STEP
         self.right+= TRIM_STEP
         angl=int(ANGL_GAIN*(self.right-self.left))
         self.csv.run(angl)

      if ch == "k" :
         #TRIM_STEP=int(0.5*(self.left+self.right)*1.0)
         self.left+= TRIM_STEP
         self.right-= TRIM_STEP
         angl=int(ANGL_GAIN*(self.right-self.left))
         self.csv.run(angl)

      if ch == "g" :
         self.left=int(0.5*(self.left+self.right)*1.0)
         self.right=self.left
         self.csv.run(0)

      if ch == "l" :
         HANDLE_STEP=int(0.5*(self.left+self.right)*2.0)
         self.left+= HANDLE_STEP
         self.right-= HANDLE_STEP
         Run(self.mL,self.mR,self.left,self.right)
         time.sleep(HANDLE_TIME)
         self.left-= HANDLE_STEP
         self.right+= HANDLE_STEP

      if ch == "h" :
         HANDLE_STEP=int(0.5*(self.left+self.right)*2.0)
         self.left-= HANDLE_STEP
         self.right+= HANDLE_STEP
         Run(self.mL,self.mR,self.left,self.right)
         time.sleep(HANDLE_TIME)
         self.left+= HANDLE_STEP
         self.right-= HANDLE_STEP

      if ch == "f" :
         self.left+= STEP
         self.right+= STEP

      if ch == "d" :
         self.left-= STEP
         self.right-= STEP
      if ch == "s" :
         self.left= 0
         self.right= 0
         self.csv.run(0)

      Run(self.mL,self.mR,self.left,self.right)
      print("\r %4d %4d" % (self.left,self.right),end='')
  


   def stop(self):
      self.mL.run(0)
      self.mR.run(0)
      self.csv.run(0)

def Run(mL,mR,left,right):
   if left<-100: left = -100
   if left>100: left = 100
   mL.run(left)
   if right<-100: right = -100
   if right>100: right = 100
   mR.run(right)


if __name__=="__main__":

   SLEEP=0.1
   ssr3=SsrRc()

   key = keyin.Keyboard()
   ch="c"
   print("Input q to stop.")
   while ch!="q":
      ch = key.read()
      try:
         ssr3.update(ch)
         time.sleep(SLEEP)
      except KeyboardInterrupt:
         ssr3.stop()
         break

   print("\nTidying up")
   ssr3.stop()
