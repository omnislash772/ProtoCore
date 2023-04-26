from InputSources import InputSource
import sounddevice, numpy

class MicSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        if "gain" in kwargs.keys() and (isinstance(kwargs["gain"], float) or isinstance(kwargs["gain"], int)):
            self.gain = kwargs["gain"]
        else:
            self.gain = 1.0
        if "inputdevice" in kwargs.keys() and isinstance(kwargs["inputdevice"], str):
            deviceList = list(sounddevice.query_devices())
            deviceName = kwargs["inputdevice"]
            if len([d for d in deviceList if d['name'] == deviceName]) > 0:
                self.inputdevice = kwargs["inputdevice"]
            else:
                self.inputdevice = sounddevice.query_devices()[sounddevice.default.device[0]]["name"]
                print(self.name + ": Invalid 'inputdevice' specified in Args, using default: " + self.inputdevice)
        else:
            self.inputdevice = sounddevice.query_devices()[sounddevice.default.device[0]]["name"]
            print(self.name + ": No 'inputdevice' specified in Args, using default: " + self.inputdevice)
        
        self.stream = sounddevice.InputStream(callback=self.audio_callback, device=self.inputdevice)
        
        self.voiceCounter = 0
        self.maxvol = 0
        self.last_voice_state = 0
        self.current_voice_state = 0
        self.state = 0

        self.stream.start()
    
    def audio_callback(self, indata, frames, time, status):
        if self.voiceCounter % 5 != 0:
            self.state = min(int(self.maxvol/5), 4)
            self.maxvol = 0
        
        volumeNorm = int(numpy.linalg.norm(indata) * 10 * self.gain)
        if volumeNorm > self.maxvol:
            self.maxvol = volumeNorm
        self.voiceCounter += 1    

    
    def getValues(self):
        return {self.name + ".State": self.state, self.name + ".MaxVol": self.maxvol}