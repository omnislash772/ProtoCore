#Simple test script to check boop sensor 
import board
import busio
import math
import adafruit_vl53l0x
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)
#change the below two to adjust the trigger window for detecting a boop
#You can use these as part of configuring BoopSense.py to trigger consistently.
MinRange=20
MaxRange=150
def boopdetect():
    while True :
     ran = sensor.range
     boop = False
     if ran > MinRange and MaxRange < 150:
       boop = True
     print('Range: {}mm'.format(ran))
     print(boop)
while True:    
 try:
  boopdetect()
 except:
    pass
