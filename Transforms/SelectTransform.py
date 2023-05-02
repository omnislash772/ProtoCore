from Transforms import Transform
from PIL import Image

class SelectTransform(Transform.Transform):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.defaultFrame = Image.new(mode="RGBA", size=(1,1))

    def process(self, inputFrames, vars):
        if type(self.select) == str:
            if self.select in vars.keys() and type(vars[self.select]) == int:
                inputId = (vars[self.select] + self.offset) % len(self.inputs)
                return inputFrames[self.inputs[inputId]]
        elif type(self.select) == int:
            return inputFrames[self.inputs[(self.select + self.offset) % len(self.inputs)]]

        return self.defaultFrame

    def getArgs(self):
        return {
            "inputs": {
                "types": [list]
            },
            "select": {
                "types": [int, str]
            },
            "offset": {
                "types": [int],
                "default": 0
            }
        }