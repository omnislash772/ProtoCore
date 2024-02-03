from Outputs import Output
from PIL import Image,ImageSequence
from PIL.Image import Resampling
import threading, time
import spidev

class ST7789Output(Output.Output):
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        from luma.core.interface.serial import gpio_cs_spi # type: ignore
        from luma.core.render import canvas # type: ignore
        from luma.lcd.device import st7789 # type: ignore

        self.serial = gpio_cs_spi(port=0, device=0, gpio_DC=self.dcPin, gpio_RST=self.rstPin, gpio_CS=self.csPin)
        self.device = st7789(self.serial, width=self.width + abs(self.xBuffer), height=self.height + abs(self.yBuffer), rotate=self.rotate)
# This makes the display run at a usable framerate as opposed to 1-2 fps       
        spi = spidev.SpiDev()
        spi.open(0,0)
        spi.max_speed_hz=(20000000)
# Lets load a boot screen while we wait for the other modules and config to load
        self.boot = Image.open("Images/HUD/BootScreen.gif")
        self.bsize=(self.height + abs(self.yBuffer), self.width + abs(self.xBuffer))
        for bframe in ImageSequence.Iterator(self.boot):
            biggerFrame = Image.new(mode="RGB", size=(self.height + abs(self.yBuffer), self.width + abs(self.xBuffer)))
            biggerFrame.paste(bframe, (max(self.xBuffer, 0), max(self.yBuffer, 0)))
            self.device.display(biggerFrame)



    def getName(self):
        return "ST7789 output"
    
    def Input(self, frame):
        self.DrawFrame(frame)
        
    def DrawFrame(self, frame):
        if self.xBuffer == 0 and self.yBuffer == 0:
            self.device.display(frame)
            return

        if self.rotate % 2 == 1: #Is odd
            biggerFrame = Image.new(mode="RGB", size=(self.height + abs(self.yBuffer), self.width + abs(self.xBuffer)))
            biggerFrame.paste(frame, (max(self.yBuffer, 0), max(self.xBuffer, 0)))
            self.device.display(biggerFrame)
        else:
            biggerFrame = Image.new(mode="RGB", size=(self.width + abs(self.xBuffer), self.height + abs(self.yBuffer)))
            biggerFrame.paste(frame, (max(self.xBuffer, 0), max(self.yBuffer, 0)))
            self.device.display(biggerFrame)
    
    def getArgs(self):
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
            #Data PIN (Some modules mark this as SDA) 
            "dcPin": {
                "types": [int],
                "default": 24
            },
            #Reset Pin(Some modules mark this as RES)
            "rstPin": {
                "types": [int],
                "default": 25
            },
            #Chip Select(CS)
            "csPin": {
                "types": [int],
                "default": 8
            },
            "width": {
                "types": [int],
                "default": 240
            },
            "height": {
                "types": [int],
                "default": 240
            },
            "rotate": {
                "types": [int],
                "default": 0
            },
            #This is needed to allow for the display to operate correctly, using the actual pixel size in the width and height options causes sections at the top or bottom to be unusable 
            "xBuffer": {
                "types": [int],
                "default": 0
            },
            "yBuffer": {
                "types": [int],
                "default": 0
            }
        }
