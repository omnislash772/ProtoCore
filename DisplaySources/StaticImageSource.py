from DisplaySources import DisplaySource
from PIL import Image
import numpy as np
from Utils import ImageUtils

class StaticImageSource(DisplaySource.DisplaySource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.fileName = kwargs["fileName"]
        self.image = ImageUtils.LoadImage(self.fileName).convert("RGBA")
    
    def Output(self, vars):
        return self.image
    
    def getName(self):
        return f"Static Image Source: '{self.fileName}'"