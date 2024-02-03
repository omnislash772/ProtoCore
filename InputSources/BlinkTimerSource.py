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
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
            "Module": {
                "Name": "BlinkTimerSource",
                "info": "Random blink timer Module",
                "class": "inputmodule", 
                "types": [int, float],
                "default": 1

            },
            "blinkTime": {
                "info": "Used to define how long a blink takes to execute",
                "class": "input", 
                "types": [float, int],
                "default": 0.2
            },
            "frameCount": {
                "info": "Defines how many frames are in your blink animations, blink animations must never be shorter than this value",
                "class": "input", 
                "types": [int],
                "default": 7
            },
            "blinkMinDelay": {
                "info": "Minimum amount of time in seconds between blinks",
                "class": "input", 
                "types": [float, int],
                "default": 5
            },
            "blinkMaxDelay": {
                "info": "Maximum amount of time between blinks",
                "class": "input", 
                "types": [float, int],
                "default": 7
            },
            "Frame": {
                "info": "Used to define what frame of the blink animation to display",
                "class": "Output", 
                "types": [float, int],
                "default": 0
            },
        }