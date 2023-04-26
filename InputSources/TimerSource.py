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
        return {
            "resolution": {
                "types": [int],
                "default": None
            }
        }