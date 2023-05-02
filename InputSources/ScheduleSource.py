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
        return {
            "events": {
                "types": [list]
            },
            "eventCount": {
                "types": [int],
                "default": 2
            },
            "delemiter": {
                "types": [str],
                "default": "\n"
            }
        }