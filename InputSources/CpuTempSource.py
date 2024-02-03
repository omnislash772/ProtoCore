from InputSources import InputSource
import os

class CpuTempSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.hasFile = False
        if os.path.isfile(self.TempPath):
            self.hasFile = True
    
    def getValues(self):
        temp = "??"
        if self.hasFile:
            temp = int(int(open(self.TempPath).read(5))/1000)
        return {self.name + ".Value": temp}
    
    def getArgs(self):
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
          "Module": {
                "Name": "CpuTempSource",
                "info": "Module to get the current CPU temperature",
                "class": "inputmodule", 
                "types": [int, float],
                "default": 1
            },
            "TempPath": {
                "info": "Path to the linux temperature zone for the CPU",
                "class": "input", 
                "types": [str],
                "default": "/sys/class/thermal/thermal_zone0/temp"
            },
            "Value": {
                "info": "Current temperature",
                "class": "Output", 
                "types": [int,float],
                "default": 22.3
            }
        }