from InputSources import InputSource
import time, math, random

class BlinkTimerSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        
        self.startTime = time.time()
        self.blinkTimer = 0
    
    def getValues(self):
        t = time.time()-self.startTime

        timeSinceStart = t - self.blinkTimer
        if timeSinceStart < 0:
            return {self.name + ".Frame": 0}
        
        interval = self.blinkTime / self.frameCount
        frame = int((math.floor(timeSinceStart*(1/interval))/(1/interval))/interval)

        if frame > self.frameCount:
            self.blinkTimer = t + (random.randint(self.blinkMinDelay * 10, self.blinkMaxDelay * 10)/10)
            frame = self.frameCount

        return {self.name + ".Frame": frame%self.frameCount}
    
    def getArgs(self):
        return {
            "blinkTime": {
                "types": [float, int],
                "default": 0.2
            },
            "frameCount": {
                "types": [int],
            },
            "blinkMinDelay": {
                "types": [float, int],
                "default": 5
            },
            "blinkMaxDelay": {
                "types": [float, int],
                "default": 7
            }
        }