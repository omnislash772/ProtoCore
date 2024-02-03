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
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
            "Module": {
                "Name": "ClockSource",
                "info": "Simple Time/Date Source",
                "class": "inputmodule", 
                "types": [int, float],
                "default": 1
            },
            "timeFormat": {
                "info": "What format to display the time in",
                "class": "input", 
                "types": [str],
                "default": "%I:%M %p"
            },
            "dateFormat": {
                "info": "What format to display the date in",
                "class": "input", 
                "types": [str],
                "default": "%d-%m-%Y"
            },  
            "Clock": {
                "info": "The current time",
                "class": "output", 
                "types": [str],
                "default": "10:04PM"
            }, 
            "Date": {
                "info": "The current date",
                "class": "output", 
                "types": [str],
                "default": "12-11-1955"
            },         
        }
    