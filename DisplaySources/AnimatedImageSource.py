from DisplaySources import DisplaySource
from PIL import Image
import time
from Utils import ImageUtils

class AnimatedImageSource(DisplaySource.DisplaySource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        if "fileName" not in kwargs.keys():
            print(self.name + ": No 'fileName' specified")
            return
        if "sourceVar" not in kwargs.keys() and "fps" not in kwargs.keys():
            print(self.name + ": no 'sourceVar' or 'fps' specified")
            return

        self.init = True
        if "fps" in kwargs.keys():
            self.fps = kwargs["fps"]
            self.startTime = time.time()
            self.sourceVar = None
        else:
            self.fps = None
            self.sourceVar = kwargs["sourceVar"]
        
        self.fileName = kwargs["fileName"]
        self.image = ImageUtils.LoadImage(self.fileName)

        self.imageframes = []
        for i in range(self.image.n_frames):
            self.image.seek(i)
            self.imageframes.append(self.image.copy().convert("RGBA"))
    
    def Output(self, vars):
        if self.fps != None:
            frame = int((time.time()-self.startTime)/(1/self.fps)) % self.image.n_frames
            return self.imageframes[frame]
        return self.imageframes[int(vars[self.sourceVar]) % self.image.n_frames]
    
    def getName(self):
        return f"Static Image Source: '{self.fileName}'"