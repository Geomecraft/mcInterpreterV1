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
        self.sysIndexMax = 1000
        # self.sysIndexFunctionalityRecord = SysIndexFunctionalityRecord() #dictionary, with the string of the functionality to map to a list of the index used
        self.flags = Flags()

    def getCurrentNamespacePath(self):
        return self.dataPackName + "/data/" + self.currentNamespace




    def getIndex(self):
        return str(self.sysIndex)

    def increment(self):
        self.sysIndex += 1

class Flags:
    def __init__(self):
        self.onLandSnowball = False
        self.onRightClick = False

#unused?
# class SysIndexFunctionalityRecord:
#     def __init__(self):
#         self.playerAction = []
#
#     def addPlayerActionScore(self, *los):
#         for x in los:
#             self.playerAction.append(x)