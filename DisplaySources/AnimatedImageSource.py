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
        self.frameCount = self.image.n_frames
        for i in range(self.frameCount):
            self.image.seek(i)
            self.imageframes.append(self.image.copy().convert("RGBA"))
    
    def Output(self, vars):
        if self.sourceVar == "default":
            if self.loopOverflow:
                frame = int((time.time()-self.startTime)/(1/self.fps)) % self.frameCount
                return self.imageframes[frame]
            else:
                frame = min(int((time.time()-self.startTime)/(1/self.fps)), self.frameCount)
                return self.imageframes[frame]
        
        if self.loopOverflow:
            return self.imageframes[int(vars[self.sourceVar]) % self.frameCount]
        else:
            return self.imageframes[min(int(vars[self.sourceVar]), self.frameCount)]
    
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
            },
            "loopOverflow": {
                "types": [bool],
                "default": True
            }
        }