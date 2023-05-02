from Transforms import Transform
from PIL import ImageDraw, ImageFont

class MultiTextOverlayTransform(Transform.Transform):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.input = self.inputs[0]["name"]
        self.textError = False
        self.texts = self.processTextsList()
    
    
    def __hexColor(self, hexValue):
        if hexValue.startswith("#"):
            hexValue = hexValue[1:]
        r,g,b = bytes.fromhex(hexValue)
        return (r, g, b)
        
    
    def process(self, inputFrames, vars):
        img = inputFrames[self.input].copy()
        frame = ImageDraw.Draw(img)

        for t in self.texts:
            text = t["text"]
            try:
                text = t["text"].format(vars)
            except Exception as e:
                if not self.textError:
                    print(self.name + ": Bad Text Format - " + repr(e))
                    self.textError = True
            
            frame.text((t["offsetX"], t["offsetY"]), text, self.__hexColor(t["color"]), font=t["font"], align=t["align"], anchor=t["anchor"])
        return img
    

    def processTextsList(self):
        if type(self.texts) == dict:
            self.texts = [self.texts]
        
        texts = []
        for text in self.texts:
            if "text" not in text.keys():
                print(f"{self.name}: Argument 'text' not defined and is required!")
                raise SystemExit(1)
            
            font = text.get("font", "default")
            if font == "default":
                font = ImageFont.load_default()
            else:
                font = ImageFont.truetype(font, text.get("fontSize", 10))
            texts.append({
                "font": font,
                "offsetX": text.get("offsetX", 0),
                "offsetY": text.get("offsetY", 0),
                "text": text.get("text"),
                "color": text.get("color", "#FFFFFF"),
                "align": text.get("align", "left"),
                "anchor": text.get("anchor", None)
            })
        return texts
            

    def getArgs(self):
        return {
            "inputs": {
                "types": [list, str]
            },
            "texts": {
                "types": [dict, list]
            }
        }