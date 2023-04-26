import abc

class Output():
    def __init__(self, name, **kwargs):
        self.name = name

        for arg in self.getArgs().keys():
            value = kwargs.get(arg, None)

            if value == None:
                if "default" not in self.getArgs()[arg].keys():
                    print(f"{self.name}: Argument '{arg}' not defined and is required!")
                    raise SystemExit(1)
                value = self.getArgs()[arg]["default"]
            
            if type(value) not in self.getArgs()[arg]['types']:
                print(f"{self.name}: Argument '{arg}' is the wrong type, expecting {self.getArgs()[arg]['types']}, got {type(arg).__name__}!")
                raise SystemExit(1)
            
            setattr(self, arg, value)

    @abc.abstractclassmethod
    def Input(self, frame):
        pass
    
    @abc.abstractclassmethod
    def getName(self):
        return "Base Output"
    
    @abc.abstractclassmethod
    def getArgs(self):
        pass