from Outputs import Output
from PIL import Image, ImageOps

class NeoPixelOutput(Output.Output):
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        import neopixel, board # type: ignore
        if type(self.pin) == int:
            self.pin = "D" + str(self.pin)
        self.pin = getattr(board, self.pin)

        self.rings = neopixel.NeoPixel(self.pin, self.chainCount * self.ledCount)
        self.rings.fill((0,0,0))

    def getName(self):
        return "NeoPixelOutput"
    
    def Input(self, frame):
        for i in range(self.ledCount):
            pix = frame.getpixel((i, 0))
            for ring in range(self.chainCount):
                self.__set_led(ring, i, pix)
    
    def __set_led(self, ringId, ledNo, data):
        if self.mirror:
            if ringId > self.chainCount/2:
                ledNo = self.ledCount - ledNo
        self.rings[(ledNo % self.ledCount) + (ringId * self.ledCount)] = data
    
    def getArgs(self):
        return {
            "pin": {
                "types": [str, int]
            },
            "ledCount": {
                "types": [int]
            },
            "chainCount": {
                "types": [int],
                "default": 1
            },
            "mirror": {
                "types": [bool],
                "default": False
            }
        }