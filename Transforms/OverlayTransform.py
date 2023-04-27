from Transforms import Transform

class OverlayTransform(Transform.Transform):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
    
    def process(self, inputFrames, vars):
        img = None
        for i in self.inputs:
            if i["name"] not in inputFrames.keys():
                print(f"Transform Input '{i['name']} not found, ignoring'")
                continue

            frame = inputFrames[i["name"]].copy()
            if img == None:
                img = frame
                continue

            x = 0
            y = 0
            if "x" in i.keys():
                x = i["x"]
            if "y" in i.keys():
                y = i["y"]
            try:
                img.paste(frame, (x, y), frame)
            except ValueError:
                img.paste(frame, (x, y))
        return img

    def getArgs(self):
        return {
            "inputs": {
                "types": [list]
            }
        }