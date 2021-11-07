#!/usr/bin/python3

# 手動でカメラの向きを変えられる。tofセンサーの値を出力できる。

# ssr109a.py
# Yasushi Honda 2021 9/3

# How to execute
# sudo pigpiod
# pyhton3 rcXY.py 

import modules.keyin as keyin # キーボード入力を監視するモジュール
import modules.rc3b_anezaki as rc
import time
import math
import modules.vl53_4a as lidar #tofセンサーのモジュール

gamma=0.50 
start = time.time()
now = start

def tanh1(x):
    alpha=0.0
    alpha2=1.0
    beta=0.4 # 0.004
    beta2=1000.00
    b=0.3  # 280
    c=0.0
    f=(alpha*math.tanh(beta*(x-b)) + alpha2*math.tanh(beta2*(x-b))+c) / (alpha + alpha2 + c)
    return f

def tanh2(x):
    alpha=0.0
    alpha2=1.0
    beta=0.4 # 0.004
    beta2=1000.00
    b=0.4  # 360
    c=0.0
    f=(alpha*math.tanh(beta*(x-b)) + alpha2*math.tanh(beta2*(x-b))+c) / (alpha + alpha2 + c)
    return f

SLEEP=0.1
ssr3=rc.KeyAssign()

key = keyin.Keyboard()
ch="c"
print("Input q to stop.")
tofL,tofR,tofC=lidar.start() #  赤外線レーザ(3)

while ch!="q":
   ch = key.read()
   print("\n")
   try:
      ssr3.update(ch)
      #time.sleep(SLEEP)
      
#tofセンサーの値を出力↓
      
      lidar_distanceL=tofL.get_distance()/1000
      if lidar_distanceL>2:
            lidar_distanceL=2

      lidar_distanceC=tofC.get_distance()/1000
      if lidar_distanceC>2:
         lidar_distanceC=2
           
      lidar_distanceR=tofR.get_distance()/1000
      if lidar_distanceR>2:
         lidar_distanceR=2

      if lidar_distanceL>0 and lidar_distanceC>0:
         areaL=math.exp(gamma*math.log(lidar_distanceC))*math.exp((1-gamma)*math.log(lidar_distanceL))
      if lidar_distanceR>0 and lidar_distanceC>0:
         areaR=math.exp(gamma*math.log(lidar_distanceC))*math.exp((1-gamma)*math.log(lidar_distanceR))

      tof_r = tanh1(areaL)
      tof_l = tanh2(areaR)
      #print("\r %6.2f " % (now-start),end="")
      
        #print(" dist=%6.2f " % dist, end="")
        #print(" theta=%6.2f " % theta, end="")
      
      print(" dL=%6.2f " % lidar_distanceL, end="")
      print(" dC=%6.2f " % lidar_distanceC, end="")
      print(" dR=%6.2f " % lidar_distanceR, end="")   
      
#tofセンサーの値を出力↑

   except KeyboardInterrupt:
      ssr3.stop()
      break

print("\n Bye Bye!")
ssr3.stop()
