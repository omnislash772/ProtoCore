from InputSources import InputSource
import time

class TimerSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.startTime = time.time()
    
    def getValues(self):
        t = time.time()-self.startTime
        if self.resolution != None:
            t = round(t, self.resolution)
        return {self.name + ".Timer": t}
    
    def getArgs(self):
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
            "Module": {
                "Name": "TimerSource",
                "info": "Universal Timing source",
                "class": "inputmodule", 
                "types": [int, float],
                "default": 1
            },
            "resolution": {
                "info": "Time resolution, defined by how many decimal places.",
                "class": "input",
                "types": [int],
                "default": None
            },
            "resolution": {
                "info": "Time resolution, defined by how many decimal places.",
                "class": "output",
                "types": [int],
                "default": None
            }
        }