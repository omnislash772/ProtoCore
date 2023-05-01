from Outputs import Output
from PIL import Image, ImageOps
try:
    import neopixel, board # type: ignore
except:
    pass

class NeoPixelOutput(Output.Output):
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        if type(self.pin) == int:
            self.pin = "D" + str(self.pin)
        self.pin = getattr(board, self.pin)

        self.rings = neopixel.NeoPixel(self.pin, self.chainCount * self.ledCount, auto_write=False)
        self.fakeRings = [(0,0,0)] * self.chainCount * self.ledCount
        self.rings.fill((0,0,0))

    def getName(self):
        return "NeoPixelOutput"
    
    def Input(self, frame):
        for i in range(self.ledCount):
            pix = frame.getpixel((i, 0))
            for ring in range(self.chainCount):
                self.__set_led(ring, i, pix)
        self.rings.show()
    
    def __set_led(self, ringId, ledNo, data):
        data = data[:3]
        if self.mirror:
            if ringId > self.chainCount/2:
                ledNo = self.ledCount - ledNo
        ledId = (ledNo % self.ledCount) + (ringId * self.ledCount)
        if self.fakeRings[ledId] != data:
            self.fakeRings[ledId] = data
            self.rings[ledId] = data
    
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