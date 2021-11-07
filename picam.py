#! /usr/bin/python3
# Yasushiu Honda 2021 9/8
# Capture frames from PiCamera and record them to /tmp 

import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import modules.keyin as keyin

class PI_CAMERA():
   def __init__(self,width,height):
      
      # カメラの解像度 例：640x480, 320x240
      self.RES_X=int( width )
      self.RES_Y=int( height )
      
      # initialize the camera and grab a reference to the raw camera capture
      #カメラを初期化，カメラへのアクセス？ルート？オブジェクト作成？
      self.cam = PiCamera()
      self.cam.framerate = 30  #フレームレート
      self.cam.brightness = 60 #明るさ
      #cam.saturation = 50

      self.cam.awb_mode='auto'
      #list_awb = ['off', 'auto', 'sunlight', 'cloudy', 'shade']
      self.cam.iso=200
      self.cam.shutter_speed=1000000
      self.cam.exposure_mode = 'auto' # off, auto, fixedfps
      time.sleep(1)
      self.g = self.cam.awb_gains
      self.cam.awb_mode = 'off'
      self.cam.awb_gains = self.g

      self.cam.resolution = (self.RES_X, self.RES_Y)
      self.cam.rotation=0
      self.cam.meter_mode = 'average' # average, spot, backlit, matrix
      self.cam.exposure_compensation = 0
      self.rawCapture = PiRGBArray(self.cam, size=(self.RES_X, self.RES_Y))

      self.rawCapture.truncate(0) # clear the stream for next frame

   def capture(self):
      tmp = self.cam.capture_continuous(self.rawCapture, format="bgr", use_video_port="True")
      cap = next(tmp)
      frame = cap.array

      self.rawCapture.truncate(0) # clear the stream for next frame

      return frame


if __name__ == "__main__":
    # For recording
    record='n' # if you want record movie, select 'y' 
               # and its FPS down to 10Hz.
               # if you select 'n' FPS is 30Hz without recording.
    OUT_FILE="/tmp/output.mp4"

    PERIOD=0.2 # Indication period


    print("# Captured movie is written in %s ." % OUT_FILE)
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    record_fps=10
    width=640
    height=480
    print("# Resolution: %5d x %5d" % (width,height))
    size = (width, height)
    vw = cv2.VideoWriter(OUT_FILE, fmt, record_fps, size)

    cam = PI_CAMERA(width,height)

    key=keyin.Keyboard()
    ch='c'

    now=time.time()
    start=now
    init=now
    count=0
    print("# To stop, input 'q' in this terminal.")
    while ch!='q':
        now=time.time()
        count+=1 
        if now-init>PERIOD:
            print("\r time: %8.2f; rate:%6.2f" % (now-start,count/PERIOD), end='')
            count=0
            init=now 

        ch=key.read()
        try: 
            frame = cam.capture()
            cv2.imshow("Front View", frame)
            cv2.waitKey(1)

            if record=='y':
                vw.write(frame)

        except KeyboardInterrupt:
            print("ctrl + C ")
            cv2.destroyAllWindows()
            vw.release()

    cv2.destroyAllWindows()
    vw.release()
    print("\n # Bye-bye \n")
