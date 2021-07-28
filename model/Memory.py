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

    def getCurrentNamespacePath(self):
        return self.dataPackName + "/data/" + self.currentNamespace

