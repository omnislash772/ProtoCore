import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(5, GPIO.OUT)           # set GPIO24 as an output   
  
try:  
    while True:  
        GPIO.output(5, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
        sleep(10)                 # wait half a second  
        if GPIO.input(5):  
            print("LED just about to switch off")  
        GPIO.output(5, 0)         # set GPIO24 to 0/GPIO.LOW/False  
        sleep(10)                 # wait half a second  
        if not GPIO.input(5):  
            print ("LED just about to switch on")  
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()                 # resets all GPIO ports used by this program 
