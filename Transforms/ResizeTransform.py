from Transforms import Transform
from PIL import Image

class ResizeTransform(Transform.Transform):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.input = self.inputs[0]["name"]

    def process(self, inputFrames, vars):
        frame = inputFrames[self.input].copy()
        return frame.resize((int(frame.width*self.scale), int(frame.height*self.scale)), resample=Image.Resampling.NEAREST)

    def getArgs(self):
        return {
            "inputs": {
                "types": [list]
            },
            "scale": {
                "types": [int, float]
            }
        }