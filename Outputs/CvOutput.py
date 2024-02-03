from Outputs import Output
import numpy as np
from PIL.Image import Resampling
try:
    import cv2
except:
    pass

class CvOutput(Output.Output):
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def getName(self):
        return "Tk output"
    
    def Input(self, frame):
        frame = frame.resize((frame.width*self.scale, frame.height*self.scale), resample=Resampling.NEAREST)
        cv2.imshow(self.name, cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)) # type: ignore
        cv2.waitKey(1) # type: ignore
    
    def getArgs(self):
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
            #Defines the pixel scale for the display outputs, can be set per output.
            "scale": {
                "types": [float, int],
                "default": 1
            }
        }