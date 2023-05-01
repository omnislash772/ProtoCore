from InputSources import InputSource
import importlib.util
try:
    from Utils import UsbTempProbe # type: ignore
except:
    pass

class ExternalTempSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
    
    def getValues(self):
        temp = 99
        humid = 99
        if importlib.util.find_spec("usb") != None and UsbTempProbe.deviceAvailable():
            temp, humid = UsbTempProbe.gethotmoist() # type: ignore
        return {
            self.name + ".Temp": temp,
            self.name + ".Humid": humid}
    
    def getArgs(self):
        return {}