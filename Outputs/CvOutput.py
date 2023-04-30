from Outputs import Output
import numpy as np
from PIL.Image import Resampling

class CvOutput(Output.Output):
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        import cv2

    def getName(self):
        return "Tk output"
    
    def Input(self, frame):
        frame = frame.resize((frame.width*self.scale, frame.height*self.scale), resample=Resampling.NEAREST)
        cv2.imshow(self.name, cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)) # type: ignore
        cv2.waitKey(1) # type: ignore
    
    def getArgs(self):
        return {
            "scale": {
                "types": [float, int],
                "default": 1
            }
        }