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
        self.bankSelect = 0
        self.softBankSelect = 0
        self.BankMemory = 0
        self.boopsel = 0
        self.infosel = 0
        self.devCount = 0
        self.locked = False
        self.pawlist = []
        self.findAndRegisterPaws()
    
    def findAndRegisterPaws(self):
        devlist = os.listdir('/dev/input')
        if len(devlist) != self.devCount:
            self.pawlist = []
            for event in list(filter(lambda d: d.find("event") != -1, devlist)):
                suspect = evdev.InputDevice('/dev/input/' + event)
                if suspect.name in self.pawNames and suspect.name not in self.paws.keys():
                    self.paws.update({suspect.path: suspect})
                    self.pawlist.append(suspect)
                    self.pawcount = len(self.pawlist)
                
            self.devCount = len(devlist)
     #   

    def processButtonPresses(self, buttonPresses):
        bc = len(buttonPresses)
        if self.locked and not ("Lwrs" in buttonPresses or "Rwrs" in buttonPresses):
            return
        if bc == 1: #Single button presses
            if "Lind" in buttonPresses:
                self.softSelect -= 1
                print("lind")
            elif "Rrng" in buttonPresses:
                self.softBankSelect -= 1
                print("rrng")
            elif "Lmid" in buttonPresses:
                self.hardSelect = self.softSelect
                self.BankMemory = self.bankSelect
                print("bank memory is" + str(self.BankMemory))
                print("lmid")
            elif "Rmid" in buttonPresses:
                self.bankSelect = self.softBankSelect
                print("rmid")
                print("Bankselect" + str(self.bankSelect))
            elif "Lrng" in buttonPresses:
                self.softSelect += 1
                print("lrng")
            elif "Rind" in buttonPresses:
                self.softBankSelect += 1
                print("soft select is" + str(self.softBankSelect))
                print("rind")
            elif "Lwrs" in buttonPresses:
                self.locked = not self.locked
                print("lwrs")
            elif "Rwrs" in buttonPresses:
                self.locked = not self.locked
                print("rwrs")
            elif "Lpnk" in buttonPresses:
                print("lpnk")
                self.boopsel += 1
            elif "Rpnk" in buttonPresses:
                self.infosel += 1
    
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
                    self.findAndRegisterPaws()

        
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
            self.name + ".Locked": int(self.locked),
            self.name + ".Pawcount": len (self.pawlist),
            self.name + ".BankMemory": self.BankMemory,
            self.name + ".BankSelect": self.bankSelect,
            self.name + ".SoftBankSelect": self.softBankSelect,
            self.name + ".BoopSelect": self.boopsel,
            self.name + ".InfoSelect": self.infosel
            }
    
    def getArgs(self):
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
            "Module": {
                "Name": "PawControllerSource",
                "info": "Module to allow user input via multiple bluetooth controllers",
                "class": "inputmodule", 
                "types": [int, float],
                "default": 1
            },
            "pawNames": {
                "info": "Comma seperated list of all controllers based on their device name. Bluetooth Devices should be pre paired and trusted before this will work.",
                "class": "input", 
                "types": [list]
            },
            "buttons": {
                "info": "List of all controller button mappings in dictionary format. EG: \"304\":\"Lind\",",
                "class": "input", 
                "types": [dict],
            },
            "HardSelect": {
                "info": "Used to store the current face index to be displayed",
                "class": "output", 
                "types": [int],
                "default": 0
            },
            "SoftSelect": {
                "info": "Soft position selector to allow browsing of faces",
                "class": "output", 
                "types": [int],
                "default": 0
            },
            "Locked": {
                "info": "Locked status for the controls",
                "class": "output", 
                "types": [int],
                "default": 0
            },
            "Pawcount": {
                "info": "Lists how many connected devices match those specified in the paw names input",
                "class": "output", 
                "types": [int],
                "default": 0
            },
            "BankMemory": {
                "info": "Stores the bank information for the current displayed face",
                "class": "output", 
                "types": [int],
                "default": 0
            },
            "BankSelect": {
                "info": "Used to store current bank being viewed on HUD",
                "class": "output", 
                "types": [int],
                "default": 0
            },
            "SoftBankSelect": {
                "info": "Current bank the soft selector is pointing to",
                "class": "output", 
                "types": [int],
                "default": 0
            },
            "BoopSelect": {
                "info": "Used to cycle through current selected boop modes",
                "class": "output", 
                "types": [int],
                "default": 0
            },
            "InfoSelect": {
                "info": "Used to cycle through configured info displays",
                "class": "output", 
                "types": [int],
                "InfoSelect": 0
            },
        }
