from InputSources import InputSource
import os

class CpuTempSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.hasFile = False
        if os.path.isfile("/sys/class/thermal/thermal_zone0/temp"):
            self.hasFile = True
    
    def getValues(self):
        temp = 99
        if self.hasFile:
            temp = int(int(open("/sys/class/thermal/thermal_zone0/temp").read(5))/1000)
        return {self.name + ".Value": temp}
    
    def getArgs(self):
        return {}