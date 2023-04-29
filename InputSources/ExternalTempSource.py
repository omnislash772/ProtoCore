from InputSources import InputSource
import importlib.util

class ExternalTempSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.hasLib = False
        if importlib.util.find_spec("usb") != None:
            from Utils import UsbTempProbe # type: ignore
            self.hasLib = True
    
    def getValues(self):
        temp = 42
        humid = 69
        if self.hasLib:
            temp, humid = UsbTempProbe.gethotmoist() # type: ignore
        return {
            self.name + ".Temp": temp,
            self.name + ".Humid": humid}
    
    def getArgs(self):
        return {}