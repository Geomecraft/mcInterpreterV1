class Memory:
    def __init__(self, memory=None):
        if memory is None:
            memory = {}
        self.memory = memory    #type dict
        self.dataPackName = ""    #type string
        self.currentNamespace = ""    #type string

    def getCurrentNamespacePath(self):
        return self.dataPackName + "/data/" + self.currentNamespace

