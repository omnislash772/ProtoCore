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
        temp = "??"
        humid = "??"
        if importlib.util.find_spec("usb") != None and UsbTempProbe.deviceAvailable():
            temp, humid = UsbTempProbe.gethotmoist() # type: ignore
        return {
            self.name + ".Temp": temp,
            self.name + ".Humid": humid}
    
    def getArgs(self):
        return {
            "Module": {
                "Name": "ExternalTempSource",
                "info": "Module to allow input of TemperHUM temperature sensor data",
                "class": "inputmodule", 
                "types": [int, float],
                "default": 1
            },
            "Temp": {
                "info":"Returns the current temperature reading in celcius",
                "types": [int, float],
                "class": "output",
                "default": 1
            },
            "Humid": {
                "info":"Returns the current temperature as a percentage value",
                "types": [int, float],
                "class": "output",
                "default": 1
            }
        }