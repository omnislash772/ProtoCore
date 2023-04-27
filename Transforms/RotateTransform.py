from Transforms import Transform
from PIL import Image

class RotateTransform(Transform.Transform):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.input = self.inputs[0]["name"]

    def process(self, inputFrames, vars):
        frame = inputFrames[self.inputs].copy()
        return frame.rotate(self.rotate, Image.NEAREST, expand=1)

    def getArgs(self):
        return {
            "inputs": {
                "types": [list]
            },
            "rotate": {
                "types": [int]
            }
        }