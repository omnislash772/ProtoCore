from InputSources import InputSource
import time

class TimerSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        if "resolution" in kwargs.keys() and isinstance(kwargs["resolution"], int):
            self.resolution = kwargs["resolution"]
        else:
            self.resolution = None
        self.startTime = time.time()
    
    def getValues(self):
        t = time.time()-self.startTime
        if self.resolution != None:
            t = round(t, self.resolution)
        return {self.name + ".Timer": t}