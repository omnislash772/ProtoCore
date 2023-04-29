from InputSources import InputSource
import importlib.util

class CpuTempSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.hasLib = False
        if importlib.util.find_spec("gpiozero") != None:
            from gpiozero import CPUTemperature # type: ignore
            self.hasLib = True
    
    def getValues(self):
        cpuTemp = 42
        if self.hasLib:
            cpuTemp = int(CPUTemperature().temperature) # type: ignore
        return {self.name + ".Value": cpuTemp}
    
    def getArgs(self):
        return {}