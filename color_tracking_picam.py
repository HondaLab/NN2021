#! /usr/bin/python3
# CC BY-SA Yasushiu Honda 2018 12/15
# 変更者：山田将司 2021/04/25
# 各種パッケージ，ソースコードをインポート

import datetime
import numpy as np
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from subprocess import Popen
import file_read as fr

class PI_CAMERA_CLASS():
   def __init__(self,upper,lower):
      #self.udp = sk.UDP_Send(MY_IP, sk.PICAM_PORT)
      self.select_rect='n' # y(es)/n(o) 検出対象を選ぶかどうか
      self.imshow='y'      # y(es)/n(o) カメラ映像を表示するかどうか，VNC必須
      self.show_res='y'    # y(es)/n(o) 結果を表示(print)するかどうか
      self.PERIOD=0.01 #FPSですね
      
      self.A = 644.3
      self.B = -25.19
      self.C = 0.6182
      self.D = -2.104
      self.E = 0.2202

      self.upper = upper
      self.lower = lower
      print("cap_upper,cap_lower")
      print("  ",self.upper,"     ",self.lower)
      
      # カメラの解像度 例：640x480, 320x240
      self.RES_X=int( 320 )
      self.RES_Y=int( 320 )
      
      # initialize the camera and grab a reference to the raw camera capture
      #カメラを初期化，カメラへのアクセス？ルート？オブジェクト作成？
      self.cam = PiCamera()
      self.cam.framerate = 30  #フレームレート
      self.cam.brightness = 60 #明るさ
      #cam.saturation = 60
      #cam.exposure_compensation = 0
      #print(cam.exposure_compensation)

      self.cam.awb_mode='auto'
      
      self.cam.awb_mode='auto'
      #　コントラスト設定かな？
      #   #Auto White Balance :list_awb = ['off', 'auto', 'sunlight', 'cloudy', 'shade']
      self.cam.iso=400
      self.cam.shutter_speed=1000000
      self.cam.exposure_mode = 'off' # off, auto, fixedfps
      time.sleep(3)
      self.g = self.cam.awb_gains
      self.cam.awb_mode = 'off'
      self.cam.awb_gains = self.g

      self.cam.resolution = (self.RES_X, self.RES_Y)
      self.cam.rotation=0
      self.cam.meter_mode = 'average' # average, spot, backlit, matrix
      self.cam.exposure_compensation = 0
      self.rawCapture = PiRGBArray(self.cam, size=(self.RES_X, self.RES_Y))

      self.rawCapture.truncate(0) # clear the stream for next frame

      # UDP send object
      #udp=sk.UDP_Send(sk.ROBOT_ADDR, sk.PICAM_PORT)
      #udp2mpl53=sk.UDP_Send(sk.MLTPICAM_BASE_ADDR, sk.PICAM22MPL53_PORT)

      self.data=[0,0,0,0,0] # For UDP socket

   def calc_dist_theta(self,lower,upper):
      tmp = self.cam.capture_continuous(self.rawCapture, format="bgr", use_video_port="True")
      cap = next(tmp)
      frame = cap.array
      frame = frame[self.upper:self.lower,:,:]
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      mask = cv2.inRange(hsv, lower, upper)
      image, contours, hierarchy  = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      rects = []
      for contour in contours:
         approx = cv2.convexHull(contour)
         rect = cv2.boundingRect(approx)
         rects.append(np.array(rect))
    
      if len(rects) > 0:
         rect = max(rects, key=(lambda x: x[2] * x[3]))
         cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)
         self.data=list(rect)
         self.data[0]=self.data[0] # レンズのズレ補正
         px=self.data[0]
         py=self.data[1]
         width = self.data[2]
         height = self.data[3]
         cpx = px + (width/2) #画像のセンター(x)
         cpy = py + (height/2) #画像のセンター(y)
         rad = (cpx-160)*(52/160)*(np.pi/180)
         angle = np.rad2deg(rad)
         dis = (self.A/(width**self.C)) + self.B + (self.D*(abs(rad)**self.E))
         dis = float(dis/100)
         #print("\r %6.4f %6.4f" % (angle, dis ), end="" )
         self.rawCapture.truncate(0) # clear the stream for next frame
      else: #red cup not capture
         dis = None
         rad = None
      self.rawCapture.truncate(0) # clear the stream for next frame
      return dis, rad, frame

   def calc_hsv(self):
      tmp = self.cam.capture_continuous(self.rawCapture, format="bgr", use_video_port="True")
      cap = next(tmp)
      frame = cap.array

      #frame = rawCapture.array
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      bbox = (0,0,10,10)
      bbox = cv2.selectROI(frame, False)
      #ok = tracker.init(frame, bbox)
      #print(bbox)
      x=int(bbox[0]+bbox[2]/2)
      y=int(bbox[1]+bbox[3]/2)
      print("hsv: %4d %4d %4d" % (hsv[y,x,0],hsv[y,x,1],hsv[y,x,2]))
      self.rawCapture.truncate(0) # clear the stream for next frame
      cv2.destroyAllWindows()

      h_range=10 # 色相の許容範囲
      s_range=50 # 彩度の許容範囲
      v_range=50 # 明度の許容範囲
      #cvtColorでつくったhsv配列はy,xの順序なので注意
      hL=hsv[y,x,0]-h_range
      hU=hsv[y,x,0]+h_range
      sL=hsv[y,x,1]-s_range
      if sL < 0:
          sL = 0
      sU=hsv[y,x,1]+s_range
      if sU > 255:
          sU = 255
      vL=hsv[y,x,2]-v_range
      if vL < 0:
          vL = 0
      vU=hsv[y,x,2]+v_range
      if vU > 255:
          vU = 255
      lower_light=np.array([hL,sL,vL])
      upper_light=np.array([hU,sU,vU])
      print(lower_light,upper_light)
      
      return lower_light,upper_light
       

if __name__ == "__main__":
    select_hsv="y"     
    FRAME_SIZE = "/home/pi/2DOVR/framesize.csv"
    upper,lower = fr.read_framesize(FRAME_SIZE)
    picam = PI_CAMERA_CLASS(upper,lower)
    count = 0
    if select_hsv=='y':
       lower_light,upper_light=picam.calc_hsv()
    else:
       #Red Cup H:S:V=3:140:129
       # h,s,v = 171,106,138
       H = 172; S = 150; V = 122
       h_range = 10; s_range = 50; v_range = 50 # 明度の許容範囲
       hL=H-h_range
       hU=H+h_range
       sL=S-s_range
       if sL < 0:
           sL = 0
       sU=S+s_range
       if sU > 255:
           sU = 255
       vL=V-v_range
       if vL < 0:
           vL = 0
       vU=V+v_range
       if vU > 255:
           vU = 255
       lower_light=np.array([hL,sL,vL])
       upper_light=np.array([hU,sU,vU])
    key = cv2.waitKey(1)
    
    
    
    
    while key!=ord('q'):
        try: 
            #picam.calc_dist_theta(lower_light,upper_light)
            dis, rad, frame = picam.calc_dist_theta(lower_light, upper_light)
            cv2.imshow("test", frame)
            cv2.waitKey(1)
        except KeyboardInterrupt:
            print("ctrl + C ")
            cv2.destroyAllWindows()


