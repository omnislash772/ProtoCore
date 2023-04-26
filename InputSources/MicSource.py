from InputSources import InputSource
import sounddevice, numpy

class MicSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        deviceList = [d["name"] for d in sounddevice.query_devices()]
        if self.inputDevice == "default":
            self.inputDevice = deviceList[sounddevice.default.device[0]]

        if self.inputDevice not in deviceList:
            self.inputDevice = deviceList[sounddevice.default.device[0]]
            print(self.name + ": Invalid 'inputDevice' specified in Args, using default: " + self.inputDevice)
        
        self.stream = sounddevice.InputStream(callback=self.audio_callback, device=self.inputDevice)
        
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
    
    def getArgs(self):
        return {
            "gain": {
                "types": [int, float],
                "default": 1
            },
            "inputDevice": {
                "types": [str],
            }
        }