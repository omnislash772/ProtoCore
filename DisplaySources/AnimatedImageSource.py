from DisplaySources import DisplaySource
from PIL import Image
import time
from Utils import ImageUtils

class AnimatedImageSource(DisplaySource.DisplaySource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.init = True
        if self.sourceVar == "default":
            self.startTime = time.time()
        
        self.image = ImageUtils.LoadImage(self.fileName)

        self.imageframes = []
        for i in range(self.image.n_frames):
            self.image.seek(i)
            self.imageframes.append(self.image.copy().convert("RGBA"))
    
    def Output(self, vars):
        if self.sourceVar == "default":
            frame = int((time.time()-self.startTime)/(1/self.fps)) % self.image.n_frames
            return self.imageframes[frame]
        return self.imageframes[int(vars[self.sourceVar]) % self.image.n_frames]
    
    def getName(self):
        return f"Static Image Source: '{self.fileName}'"

    def getArgs(self):
        return {
            "fileName": {
                "types": [str]
            },
            "sourceVar": {
                "types": [str],
                "default": "default"
            },
            "fps": {
                "types": [int, float],
                "default": 30
            }
        }