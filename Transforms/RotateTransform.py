from Transforms import Transform
from PIL import Image

class RotateTransform(Transform.Transform):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        
        if "inputs" not in kwargs.keys() or (not isinstance(kwargs["inputs"], list) and not isinstance(kwargs["inputs"], str)):
            print(self.name + ": Missing inputs or inputs not list")
        if isinstance(kwargs["inputs"], list):
            self.inputs = kwargs["inputs"][0]
        else:
            self.inputs = kwargs["inputs"]
        
        if "rotate" not in kwargs.keys() or not isinstance(kwargs["rotate"], int):
            print(self.name + ": Needs arg 'rotate' as int")
        else:
            self.rotate = kwargs["Rotate"]
    
    def process(self, inputFrames, vars):
        frame = inputFrames[self.inputs].copy()
        return frame.rotate(self.rotate, Image.NEAREST, expand=1)