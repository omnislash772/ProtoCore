from Outputs import Output
from PIL import Image, ImageOps
try:
    import neopixel
except:
    print("failed to load neopixel module")
    pass
try:
   import  board
except:
    print("failed to load board module")
    pass
class NeoPixelOutput(Output.Output):
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        if self.pin[0] !="D":
            print("Neopixel Pin is set to:",self.pin)
            self.pin = "D" + str(self.pin)
            print("Prepending D on Pin selection, consider updating config!")
        self.pin = getattr(board, self.pin)

        self.rings = neopixel.NeoPixel(self.pin, self.chainCount * self.ledCount, auto_write=False)
        self.fakeRings = [(0,0,0)] * self.chainCount * self.ledCount
        self.rings.fill((0,0,0))

    def getName(self):
        return "NeoPixelOutput"
    
    def Input(self, frame):
      try:  
        for i in range(self.ledCount):
            pix = frame.getpixel((i, 0))
            for ring in range(self.chainCount):
                self.__set_led(ring, i, pix)
        self.rings.show()
      except:
          pass
    
    def __set_led(self, ringId, ledNo, data):
      try:  
        data = data[:3]
        if self.mirror:
            if ringId > self.chainCount/2:
                ledNo = self.ledCount - ledNo
        ledId = (ledNo % self.ledCount) + (ringId * self.ledCount)
        if self.fakeRings[ledId] != data:
            self.fakeRings[ledId] = data
            self.rings[ledId] = data
      except:
        pass
    def getArgs(self):
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
            #Used to set the data pin used to drive the Neopixels
            "pin": {
                "types": [str, int]
            },
            #This needs to match the width of all images fed to the Neopixel source and should match the amount of pixels in the chain.
            "ledCount": {
                "types": [int]
            },
            "chainCount": {
                "types": [int],
                "default": 1
            },
            #Mirror all images sent to the Neopixel
            "mirror": {
                "types": [bool],
                "default": False
            }
        }
