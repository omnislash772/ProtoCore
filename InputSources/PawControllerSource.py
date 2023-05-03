from InputSources import InputSource
import os
try:
    import evdev # type: ignore
except:
    pass

class PawControllerSource(InputSource.InputSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.paws = {}
        
        self.errorPaws = []
        self.softSelect = 0
        self.hardSelect = 0
        self.devCount = 0

        self.findAndRegisterPaws()
    
    def findAndRegisterPaws(self):
        devlist = os.listdir('/dev/input')
        if len(devlist) != self.devCount:
            for event in list(filter(lambda d: d.find("event") != -1, devlist)):
                suspect = evdev.InputDevice('/dev/input/' + event)
                if suspect.name in self.pawNames and suspect.name not in self.paws.keys():
                    self.paws.update({suspect.path: suspect})
            self.devCount = len(devlist)
        

    def processButtonPresses(self, buttonPresses):
        bc = len(buttonPresses)
        if bc == 1: #Single button presses
            if "Lind" in buttonPresses:
                self.softSelect -= 1
            elif "Rrng" in buttonPresses:
                self.softSelect -= 1
            elif "Lmid" in buttonPresses:
                self.hardSelect = self.softSelect
            elif "Rmid" in buttonPresses:
                self.hardSelect = self.softSelect
            elif "Lrng" in buttonPresses:
                self.softSelect += 1
            elif "Rind" in buttonPresses:
                self.softSelect += 1
    
    def getValues(self):
        events = []
        buttonPresses = []
        for paw in self.paws.values():
            try:
                events.append(paw.read_one())
                if paw.path in self.errorPaws:
                    self.errorPaws.remove(paw.path)
            except:
                try:
                    if paw.path not in self.errorPaws:
                        self.paws[paw.path] = evdev.InputDevice(paw.path)
                except:
                    self.errorPaws.append(paw.path)
        
        for e in events:
            if e == None:
                continue
            if e.type != evdev.ecodes.EV_KEY or e.value != 1:
                continue
            if str(e.code) in self.buttons.keys():
                buttonPresses.append(self.buttons[str(e.code)])
        
        self.processButtonPresses(buttonPresses)
        self.findAndRegisterPaws()

        return {
            self.name + ".HardSelect": self.hardSelect,
            self.name + ".SoftSelect": self.softSelect,
            }
    
    def getArgs(self):
        return {
            "pawNames": {
                "types": [list]
            },
            "buttons": {
                "types": [dict],
            }
        }