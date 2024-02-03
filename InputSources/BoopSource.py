from InputSources import InputSource
import board
import busio
import statistics
import adafruit_vl53l0x
import RPi.GPIO as GPIO
import time

class BoopSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
#Gpio code to prepare for sensor issues in long runs        
        self.ranges = [240,240]
        self.index  = 0
        self.booped = 0
        self.errors = 0
        self.Success = 0
        self.recalcheck = 0
# We need the GPIO set to BCM mode to be able to trigger the xshut switch via a transistor so lets try that
        try:
         GPIO.setmode(GPIO.BCM)
        except:
         print("BoopSense: Failed to set GPIO MODE")
        GPIO.setwarnings(False)
        GPIO.setup(self.ResetPin, GPIO.OUT)
        GPIO.output(self.ResetPin,0)
#Try to initiallize the sensor and reset it if fail
        try:
          self.i2c = busio.I2C(board.SCL, board.SDA)
          self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)
        except Exception as e:
         print("BoopSense: Sensor not ready on Init")
         GPIO.output(self.ResetPin,1)
         time.sleep(0.06)
         GPIO.output(self.ResetPin,0)



    def getValues(self):
         #Set a delay on how often to poll the sensor for data, vl53lox sensors do not like continuous polling so this may cause issues if it is called too fast
         self.index += 1
         #Delay is set based on the numbers below, default to only query the sensor on every 10th polling request
         if self.index % 10 == 0 :
           try: 
            self.ran = self.sensor.range
#uncomment the below line to allow console reports of every distance reported in mm 
#            print(str(self.ran))
# check for max distance reports as too many could indicate library needs to reinitalize.
            if self.ran == self.SensMax:
               self.recalcheck +=1
#clamp the number down to make boops more responsive on start
            if self.ran >self.DistClamp :
              self.ran = self.DistClamp
#Cleanup sensor by reinitializing it if it has reset           
            if self.ran <=self.SensMin :
             self.ran = self.DistClamp
             self.recalcheck += 1
#Recalibrate if sensors are out of spec
            if self.recalcheck >self.RecalTol :
              print("BoopSense: Anomalous readings, Recalibrating sensor")
              try:
                self.i2c = busio.I2C(board.SCL, board.SDA)
                self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)
#In case of issues lets ensure we just return that there is no boop in progress
                self.ran = self.DistClamp
              except Exception as e:
                pass
              else:
                  self.recalcheck = 0
            self.ranges.append(self.ran)
            self.Success += 1
            if self.Success > 5:
             self.errors = 0
             self.Success = 0
           except Exception as e :
             print("Boopsense: Sensor not ready,",e)
             self.errors +=1
             if self.errors >= self.ErrTol :
                print("Boopsense: Too many errors in a short time, Resetting sensor and recalibrating")
                GPIO.output(self.ResetPin,1)
                time.sleep(0.06)
                GPIO.output(self.ResetPin,0)
                self.ranges = [240,240]
                self.index  = 0
                self.booped = 0
                #time.sleep(0.2)
                self.errors = 5
                try:
                   self.i2c = busio.I2C(board.SCL, board.SDA)
                   self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)
                except:
                   print("Boopsense: Failed to call sensor")
                else:
                   self.errors = 0
         if len(self.ranges) >self.AverageLen :
               self.ranges.pop(0)
         if statistics.mean(self.ranges) >self.MinRan and statistics.mean(self.ranges) <self.MaxRan :
            self.booped = 1
         else:
           self.booped = 0
         return {self.name + ".triggered": self.booped}
    def getArgs(self):
 #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined       
        return {
          "Module": {
                "Name": "BoopSource",
                "info": "Module to detect Face boop gestures based on the vl53l0x sensor",
                "class": "inputmodule", 
                "types": [int, float],
                "default": 1
            },
          "ResetPin": {
                "info": "Pin used to trigger a reset on the Xshut input on the sensor",
                "class": "input", 
                "types": [int],
                "default": 19
            },
          "MaxRan": {
                "info": "Maximum trigger distance in mm",
                "class": "input",
                "types": [int],
                "default": 150
            },
          "MinRan": {
                "info": "Minimim trigger distance in mm",
                "class": "input",
                "types": [int],
                "default": 25
            },
          "SensMax": {
                "info": "Maximum possible reading the sensor can output, Used to determine if the sensor may be reporting bad data",
                "class": "input",
                "types": [int],
                "default": 8191
            },
          "SensMin": {
                "info": "Minimum sensor detection value, used to determine if the sensor may be reporting bad data",
                "class": "input",
                "types": [int],
                "default": 24
            },
          "ErrTol": {
                "info": "Sets how many read errors in a short period of time should trigger a sensor reset",
                "class": "input",
                "types": [float, int],
                "default": 15
            },
          "RecalTol": {
                "info": "How many Anomalous reports in a short period of time should trigger a recalibration ",
                "class": "input",
                "types": [int],
                "default": 6
            },
          "DistClamp": {
                "info": "Number to clamp the sensor readings down to in order to keep the average low, used to keep the sensor responsive",
                "class": "input",
                "types": [int],
                "default": 240
            },
          "AverageLen": {
                "info": "How long our list of past readings should be. The average of this list is used to determine if we return a true or false state, a longer list will result in a stickier result. good if you want boops to last a bit longer at the expense of a slight delay detecting them",
                "class": "input",
                "types": [int],
                "default": 4
            },
          "Triggered": {
                "info": "Output state when the average of past readings is within the minimum and maximum trigger distances, true or false",
                "class": "output",
                "types": [bool],
                "default": 0
            }
        }
