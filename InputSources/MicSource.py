from InputSources import InputSource
import sounddevice, numpy
import time
class MicSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        deviceList = [d["name"] for d in sounddevice.query_devices()]
        if self.inputDevice == "default":
            self.inputDevice = deviceList[sounddevice.default.device[0]]
#Added code to try to ensure Mic sensor is available by the time it is called in case of it not being ready on module start
        if self.inputDevice not in deviceList:
               print("Micsource: Mic not found, retrying")
               self.Miccheck=0
               while self.Miccheck <3:
                  self.Miccheck += 1
                  print("Micsource: Trying Mic, Attempt " + str(self.Miccheck) + "/6")
                  sounddevice._terminate()
                  time.sleep(0.1)
                  sounddevice._initialize()
                  deviceList.clear()
                  time.sleep(0.1)
                  deviceList = [d["name"] for d in sounddevice.query_devices()]
                  if self.inputDevice in deviceList:
                     print("Micesource: Device, ",self.inputDevice," Found!")
                     self.Miccheck = 10
                  time.sleep(0.2)               
               if self.inputDevice not in deviceList:
                 try:
                    self.inputDevice = deviceList[sounddevice.default.device[0]]
                    print(self.name + ": Invalid 'inputDevice' specified in Args, using default: " + self.inputDevice)
                 except:
                   pass
        try:
           self.stream = sounddevice.InputStream(callback=self.audio_callback, device=self.inputDevice)
        except:
           pass
        self.voiceCounter = 0
        self.maxvol = 0
        self.last_voice_state = 0
        self.current_voice_state = 0
        self.state = 0
        try:
         self.stream.start()
        except:
         pass
    def audio_callback(self, indata, frames, time, status):
        if self.voiceCounter % 5 != 0:
            self.state = min(int(self.maxvol/5), 4)
            self.maxvol = 0
        
        volumeNorm = int(numpy.linalg.norm(indata) * 10 * self.gain)
        if volumeNorm > self.maxvol:
            self.maxvol = volumeNorm
        self.voiceCounter += 1    

    
    def getValues(self):
        try:
           return {self.name + ".State": self.state, self.name + ".MaxVol": self.maxvol}
        except:
           return {self.name + ".State": "0", self.name + ".MaxVol": "0"}

    def getArgs(self):
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
            "Module": {
                "Name": "MicSource",
                "info": "Microphone input module for voice detection",
                "class": "inputmodule", 
                "types": [int, float],
                "default": 1

            },
            "gain": {
                "info":"Gain of the microphone, can be set anywhere between 0 and 1",
                "types": [int, float],
                "class": "input",
                "default": 1
            },
            "inputDevice": {
               "info":"Normalized device name as it would show when running the lsusb command",
                "types": [str],
                "class":"input",
                "default": "default"
            },
            "State": {
                "info":"Output of the microphone as represented as a volume integer from 0-100",
                "class": "output",
                "types": [int,float],
                "default": 0
            },
        }
