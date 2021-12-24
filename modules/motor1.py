#!/usr/bin/python3

# motor1.py
# 2018-11-5
# Yasushi Honda

import pigpio
import time

MIN_WIDTH=700
MID_WIDTH=1580
MAX_WIDTH=2450

class Motor:

   def __init__(self,gpio):
      self.gpio=gpio
      self.pi = pigpio.pi()
      if not self.pi.connected:
         exit()
      self.pi.set_servo_pulsewidth(gpio, MID_WIDTH)
      self.SLEEP=0.02
      #time.sleep(0.1)

   def move(self,power):
      output=MID_WIDTH+power
      if output>MAX_WIDTH:
         output=MAX_WIDTH
      if output<MIN_WIDTH:
         output=MIN_WIDTH
      self.pi.set_servo_pulsewidth(self.gpio, output)
      #print(MID_WIDTH+power)
      time.sleep(self.SLEEP)    

   def stop(self):
      self.pi.stop()

class Lmotor(Motor):
   def run(self,power):
      out=power*10
      if out>1500:
         out=1500
      if out<-1500:
         out=-1500
      self.move(-out)

class Rmotor(Motor):
   def run(self,power):
      out=power*10
      if out>1500:
         out=1500
      if out<-1500:
         out=-1500
      self.move(out)
       
if __name__=='__main__':

   # モーター出力最小値と最大値
   MIN=-100
   MAX=100

   # rate調整用の待ち時間(秒)
   SLEEP=0.2

   # LeftモーターをGPIO=18に、Rightモーターを17につなぐ。
   motorL = Lmotor(18)
   motorR = Rmotor(27)
   
   # 停止の仕方のメッセージ表示
   print("Robot runs only 1sec.")

   # 左右のモーター出力をゼロに初期化する。
   motorL.run(0)
   motorR.run(0)
   time.sleep(1)

   # 各変数の初期化
   left=0
   right=0
   start=time.time()
   now=start
   while left<100 :
      now=time.time() 
      print("\r %5d %5d " % (left,right),end='')
      motorL.run(left)
      motorR.run(right)
      time.sleep(SLEEP)
      left=left+5
      right=right+5
   while left>-100 :
      now=time.time() 
      print("\r %5d %5d " % (left,right),end='')
      motorL.run(left)
      motorR.run(right)
      time.sleep(SLEEP)
      left=left-5
      right=right-5

   # モーター出力をゼロにもどして止める
   motorL.run(0)
   motorR.run(0)
   motorL.stop()
   motorR.stop()
