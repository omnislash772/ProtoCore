import abc

class Output():
    def __init__(self, name, **kwargs):
        self.name = name

    @abc.abstractclassmethod
    def Input(self, frame):
        pass
    
    @abc.abstractclassmethod
    def getName(self):
        return "Base Output"