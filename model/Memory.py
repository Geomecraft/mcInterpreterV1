class Memory:
    def __init__(self, function=None, constant = None):
        if function is None:
            function = {}
        if constant is None:
            constant = {}
        self.function = function    #type dict
        self.constant = constant    #type dict
        self.dataPackName = ""    #type string
        self.currentNamespace = ""    #type string
        self.namespaces = [] #type listof string
        self.sysIndex = 1 #start at 1, sys 0 is for the global sys
        self.flags = Flags()

    def getCurrentNamespacePath(self):
        return self.dataPackName + "/data/" + self.currentNamespace

class Flags:
    def __init__(self):
        self.onLandSnowball = False
