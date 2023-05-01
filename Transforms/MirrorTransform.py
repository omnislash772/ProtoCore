from Transforms import Transform
from PIL import Image, ImageOps

class MirrorTransform(Transform.Transform):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.input = self.inputs[0]["name"]

    def process(self, inputFrames, vars):
        frame = inputFrames[self.input]
        return ImageOps.mirror(frame)

    def getArgs(self):
        return {
            "inputs": {
                "types": [list]
            }
        }