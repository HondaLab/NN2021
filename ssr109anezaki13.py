#!/usr/bin/python3

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


FRAME_SIZE = "/home/pi/anezaki/20211115/framesize.csv"
upper,lower = fr.read_framesize(FRAME_SIZE)



gamma=0.50
DT = 0.015
dt = DT
 
start = time.time()
now = start

select_hsv = "y" # 画面上で対象物を選択する場合は"y"
imshow = "y"

#csvはカメラのモーターのこと
GPIO_CSV = 27
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



while key!=ord('q'):
   
   
  #ここでカメラモーターを制御したい
  
   frame, cpx, maxpix = picam2.calc_dist_theta(lower_light, upper_light)
   #dist,theta,frame = picam2.calc_dist_theta(lower_light, upper_light)
   
   center_x = maxpix/2
   #center_xは映像の中心座標
   #cpxは選択枠のx軸の中心座標の値
   
   
   
#だいたい真ん中に見えてるとき #許容範囲を広めたほうがいいかも
   if center_x*0.8 <= cpx <= center_x + center_x*0.2:
      
      #csv.stop()できない
      
      #cpx = center_x
      
      print("\n")
      print("about x_pixcel_center")
   
   
      
#(右から)左へ向かせたい
   elif cpx < center_x*0.8: #0---144
      
      cpx_left = center_x*0.80 - cpx #cpx_leftはcpxとcenter*0.85の差
      mr = int( (cpx_left / center_x*0.8) * 60  ) #motor run  モーター出力

      for degree in range(mr-5, mr+6):
         dc = degree
         csv.run(dc)
         time.sleep(DT)
         if degree ==  mr+6 :
            break
      print(" csv.runの強さ= %6.2f " %mr)
      
      #少し右へ
      if cpx < center_x*0.3:
      
        cpx_left = center_x*0.80 - cpx #cpx_leftはcpxとcenter*0.85の差
        mr = int( (cpx_left / center_x*0.8) * 30  ) #motor run  モーター出力

        for degree in range(mr-5, mr+6):
          dc = degree
          csv.run(dc)
          time.sleep(DT)
          if degree ==  mr+6 :
            break
        print(" もう少し右へ= %6.2f " %mr)
      
    
      
#(左から)右へ向かせたい
   elif center_x + center_x*0.2 < cpx <= center_x*2: 
      
      #time.sleep(0.1)
      
      mr = int( (cpx/maxpix)* 60  )    #motor run  モーター出力 
     
      for degree in range(mr-5, mr+6):
         dc = -degree                  #マイナスに変換している
         csv.run(dc)
         time.sleep(DT)
         if degree == mr+6 :
            break
      print(" csv.runの強さ= - %6.2f " %mr)
      
      #少し左へ
      if center_x + center_x*0.8 < cpx:
        
        mr = int( (cpx/maxpix)* 30  )    #motor run  モーター出力 
     
        for degree in range(mr-5, mr+6):
          dc = -degree                  #マイナスに変換している
          csv.run(dc)
          time.sleep(DT)
          if degree == mr+6 :
            break
        print(" もう少こし左へ= - %6.2f " %mr)
        
      

      
   else:
      print("this is else")     
      time.sleep(0.1)
      
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
      
      print(type(cpx)) #cpxの型を出力

      print(" cpx=%6.2f " %cpx)
      
#画面に映像を出力
      if imshow == 'y':    
            cv2.imshow("frame",frame)
            key=cv2.waitKey(1)
            time.sleep(DT)
            last = now
            now = time.time()
            dt = now-last


   except KeyboardInterrupt:
      #ssr3.stop()
      break
      

print("\n")
print(" x_pixcel_center=%6.2f " %center_x)
print(" csv.runの強さ= %6.2f " %mr)
print("\n Bye Bye!")

