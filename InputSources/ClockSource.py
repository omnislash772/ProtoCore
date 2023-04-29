from InputSources import InputSource
from datetime import datetime

class ClockSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
    
    def getValues(self):
        return {
            self.name + ".Clock": datetime.now().strftime(self.timeFormat),
            self.name + ".Date": datetime.now().strftime(self.dateFormat),
            }
    
    def getArgs(self):
        return {
            "timeFormat": {
                "types": [str],
                "default": "%I:%M %p"
            },
            "dateFormat": {
                "types": [str],
                "default": "%d-%m-%Y"
            }
        }