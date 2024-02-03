from Transforms import Transform
from PIL import ImageDraw, ImageFont

class TextOverlayTransform(Transform.Transform):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.input = self.inputs[0]["name"]

        if self.font == "default":
            self.font = ImageFont.load_default()
        else:
            self.font = ImageFont.truetype(self.font, self.fontSize, self.encoding)
        self.textError = False
        if self.anchor == "none":
            self.anchor = None
    
    def __hexColor(self, hexValue):
        if hexValue.startswith("#"):
            hexValue = hexValue[1:]
        r,g,b = bytes.fromhex(hexValue)
        return (r, g, b)
        
    
    def process(self, inputFrames, vars):
        text = self.text
        try:
            text = self.text.format(vars)
        except Exception as e:
            if not self.textError:
                print(self.name + ": Bad Text Format - " + repr(e))
                self.textError = True
        
        img = inputFrames[self.input].copy()
        frame = ImageDraw.Draw(img)
        frame.text((self.offsetX, self.offsetY), text, self.__hexColor(self.color), font=self.font, align=self.align, anchor=self.anchor)
        return img

    def getArgs(self):
        return {
            "inputs": {
                "types": [list, str]
            },
            "font": {
                "types": [str],
                "default": "default"
            },
            "offsetX": {
                "types": [int],
                "default": 0
            },
            "offsetY": {
                "types": [int],
                "default": 0
            },
            "text": {
                "types": [str]
            },
            "color": {
                "types": [str],
                "default": "#FFFFFF"
            },
            "fontSize": {
                "types": [int],
                "default": 10
            },
            "align": {
                "types": [str],
                "default": "left"
            },
            "anchor": {
                "types": [str],
                "default": "none"
            },
            "encoding": {
                "types": [str],
                "default": "utf-8"
            }
        }