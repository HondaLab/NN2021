#!/usr/bin/python3

###数値(x)を手動で変えるとカメラの向きが変わる。

# ssr109a.py
# Yasushi Honda 2021 9/3

# How to execute
# sudo pigpiod
# pyhton3 rcXY.py 

#import modules.keyin as keyin # キーボード入力を監視するモジュール
import modules.rc3b_anezaki as rc
import picam2 as PICAM_py 
import file_read as fr
import modules.motor1 as sv # カメラサーボ
import modules.motor5a as mt # pwmでモーターを回転させるためのモジュール

import RPi.GPIO as GPIO

import time
import math
import modules.vl53_4a as lidar #tofセンサーのモジュール
import csv
import sys
import cv2
import datetime
import platform
import numpy as np


FRAME_SIZE = "/home/pi/2DOVR/framesize.csv"

upper,lower = fr.read_framesize(FRAME_SIZE)


gamma=0.50
DT = 0.015
dt = DT
 
start = time.time()
now = start

select_hsv = "y" # 画面上で対象物を選択する場合は"y"
imshow = "y"

#カメラ関連
STEP=8
HANDLE_STEP=8
HANDLE_TIME=0.3
TRIM_STEP=8 #カメラの振り幅調節
TRIM_TIME=0.2
ANGL_GAIN=0.6


mL=mt.Lmotor(17)
mR=mt.Rmotor(18)
csv=sv.Rmotor(27) #csvはカメラのモーターのこと
left=0
right=0

GPIO_L = 17 
GPIO_R = 18 
GPIO_CSV = 27

mL=mt.Lmotor(GPIO_L)         
mR=mt.Rmotor(GPIO_R)
csv=sv.Rmotor(GPIO_CSV)   



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



print("#-- #-- #-- #-- #-- #-- #-- #-- #--")
picam2 =PICAM_py.PI_CAMERA_CLASS(upper,lower) 
print("picamera 接続完了\n")


#色の選択はここ
if select_hsv=='y':
    lower_light,upper_light=picam2.calc_hsv()
else:
    #Red Cup H:S:V=3:140:129
    # h,s,v = 171,106,138
    #H = 171; S = 110; V =215
    # H,S,V = 173,110,215 21/10/26 VRシアター
    H = 169 ; S =188; V =214
    h_range = 10; s_range = 50; v_range = 50 # 明度の許容範囲
    hL = H - h_range
    hU = H + h_range
    sL = S - s_range
    sU = S + s_range
    vL = V - v_range
    vU = V + v_range
    if sL < 0:
        sL = 0
    if sU > 255:
        sU = 255
    if vL < 0:
        vL = 0
    if vU > 255:
        vU = 255
    lower_light = np.array([hL, sL, vL])
    upper_light = np.array([hU, sU, vU])

start = time.time()
now = start

key=cv2.waitKey(1)



SLEEP=0.1



#key = keyin.Keyboard()

ch="c"
print("Input q to stop.")
tofL,tofR,tofC=lidar.start() #  赤外線レーザ(3)

#x,y=picam2.center_xy() #映像のセンター


while key!=ord('q'):
   
   
  #ここでカメラモーターを制御したい
  
   x=11
  
   if 1<x<=10:
      #変な動きをする
      left-= TRIM_STEP
      right+= TRIM_STEP
      angl=int(ANGL_GAIN*(right-left))
      csv.run(angl)
    
   if 11<=x<20:
     #右に向く
      left+= TRIM_STEP
      right-= TRIM_STEP
      angl=int(ANGL_GAIN*(right-left))
      csv.run(angl)
   
   else:
      csv.run(0)
   
   
   
   print("\n")
   try:
      #ssr3.update(ch)
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
      dist,theta,frame = picam2.calc_dist_theta(lower_light, upper_light)
      
#画面に映像を出力
      if imshow == 'y':    
            cv2.imshow("frame",frame)
            key=cv2.waitKey(1)
            time.sleep(DT)
            last = now
            now = time.time()
            dt = now-last





   except KeyboardInterrupt:
      ssr3.stop()
      break
      
print("\n")
print("test")
print(" center_x=%6.2f " %x)
      
print("\n Bye Bye!")
ssr3.stop()
