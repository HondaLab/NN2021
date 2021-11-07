#!/usr/bin/python3
import ev3dev.ev3 as ev3
import keyin
import time

t_fwd=0.3
p_fwd=50
t_bak=0.3
p_bak=50
t_turn=0.5
p_turn=50

key=keyin.Keyboard()

mL=ev3.LargeMotor('outD')
mR=ev3.LargeMotor('outA')
mL.reset()
mR.reset()

ch='c'

while not(ch=='q' or ch=='Q') :
   print("\r q:stop; j:forwad; k:back; h:left; l:right %s" % ch,end='')
   ch=key.read()
   if ch=='j': # Move Forward
      mL.run_direct(duty_cycle_sp=p_fwd)
      mR.run_direct(duty_cycle_sp=p_fwd)
      time.sleep(t_fwd)
      mL.run_direct(duty_cycle_sp=0)
      mR.run_direct(duty_cycle_sp=0)
   if ch=='k': # Move Back
      mL.run_direct(duty_cycle_sp=-p_bak)
      mR.run_direct(duty_cycle_sp=-p_bak)
      time.sleep(t_bak)
      mL.run_direct(duty_cycle_sp=0)
      mR.run_direct(duty_cycle_sp=0)
   if ch=='h': # Turn Left
      mL.run_direct(duty_cycle_sp=-p_turn)
      mR.run_direct(duty_cycle_sp=p_turn)
      time.sleep(t_turn)
      mL.run_direct(duty_cycle_sp=0)
      mR.run_direct(duty_cycle_sp=0)
   if ch=='l': # Turn Right
      mL.run_direct(duty_cycle_sp=p_turn)
      mR.run_direct(duty_cycle_sp=-p_turn)
      time.sleep(t_turn)
      mL.run_direct(duty_cycle_sp=0)
      mR.run_direct(duty_cycle_sp=0)

print('Bye bye, see you later.')
mL.stop()
mR.stop()
