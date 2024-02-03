from InputSources import InputSource
from datetime import datetime

class ScheduleSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
    
    def getValues(self):
        events = self.events
        for e in range(len(events)):
            events[e].update({"timeDelta": (datetime.fromisoformat(events[e]["start"]) - datetime.now()).total_seconds()})
        
        filtered = list(filter(lambda e: e["timeDelta"] > 0, [e for e in events]))
        filtered.sort(key=lambda e: e["timeDelta"])
        result = self.delemiter.join([datetime.fromisoformat(x["start"]).strftime("%H%M") + ": " + x["title"] for x in filtered[:self.eventCount]])
        return {
            self.name + ".Schedule": result,
            }
    
    def getArgs(self):
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
            "Module": {
                "Name": "ScheduleSource",
                "info": "Module that shows the next X number of events based on the current time",
                "class": "inputmodule", 
                "types": [int, float],
                "default": 1
            },
            #
            "events": {
                "info": "The list of events as parsed from Json",
                "class": "input", 
                "types": [list]
            },
            #
            "eventCount": {
                "info": "How many events to display at one time",
                "class": "input", 
                "types": [int],
                "default": 4
            },
            #Define the multiline delimiting character to put text onto a new line
            "delemiter": {
                "info": "Define the multiline delimiting character to put text onto a new line",
                "class": "input", 
                "types": [str],
                "default": "\n"
            },
            "Schedule": {
                "info": "Current list of events limited by eventCount",
                "class": "output", 
                "types": [int],
                "default": 0

            },
        }