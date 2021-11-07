#!/usr/bin/python3

# ssr109a.py
# Yasushi Honda 2021 9/3

# How to execute
# sudo pigpiod
# pyhton3 rcXY.py 

import modules.keyin as keyin # キーボード入力を監視するモジュール
import modules.rc3b as rc
import time

SLEEP=0.1
ssr3=rc.KeyAssign()

key = keyin.Keyboard()
ch="c"
print("Input q to stop.")

while ch!="q":
   ch = key.read()
   try:
      ssr3.update(ch)
      #time.sleep(SLEEP)
   except KeyboardInterrupt:
      ssr3.stop()
      break

print("\n Bye Bye!")
ssr3.stop()
