from luma.core.interface.serial import gpio_cs_spi 
from luma.core.render import canvas
from luma.lcd.device import pcd8544, st7735, st7789, st7567, uc1701x, ili9341, ili9486, hd44780
from pathlib import Path
from PIL import Image, ImageSequence
from luma.core.sprite_system import framerate_regulator
import spidev
serial = gpio_cs_spi(port=0, device=0, gpio_DC=24, gpio_RST=25, gpio_CS=8)
device = st7789(serial,width=240 + abs(-20), height=280 +abs(0),rotate=1)
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=(52000000)



def do_nothing(obj):
    pass

device.cleanup = do_nothing

regulator = framerate_regulator(fps=12)
boot =  Image.new("RGB", (240,240), "black")

for frame in ImageSequence.Iterator(boot):
   with regulator:
                print("frame out")
                device.display(frame)

