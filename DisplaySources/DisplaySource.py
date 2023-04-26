import abc

class DisplaySource():
    def __init__(self, name, **kwargs):
        self.name = name

    @abc.abstractclassmethod
    def Output(self, vars):
        pass

    @abc.abstractclassmethod
    def getName(self):
        return "Base Display Source"