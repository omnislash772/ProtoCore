from Outputs import Output
from PIL import Image
from PIL.Image import Resampling
import threading, time

class ST7789Output(Output.Output):
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        from luma.core.interface.serial import gpio_cs_spi # type: ignore
        from luma.core.render import canvas # type: ignore
        from luma.lcd.device import st7789 # type: ignore

        self.serial = gpio_cs_spi(port=0, device=0, gpio_DC=self.dcPin, gpio_RST=self.rstPin, gpio_CS=self.csPin)
        self.device = st7789(self.serial, width=self.width + abs(self.xBuffer), height=self.height + abs(self.yBuffer), rotate=self.rotate)

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
        return {
            "dcPin": {
                "types": [int],
                "default": 9
            },
            "rstPin": {
                "types": [int],
                "default": 25
            },
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
            "xBuffer": {
                "types": [int],
                "default": 0
            },
            "yBuffer": {
                "types": [int],
                "default": 0
            }
        }