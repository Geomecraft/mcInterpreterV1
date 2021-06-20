class DebugLog:
    def __init__(self,loi=None,lom=None):
        self.loi = loi #list of DebugElementInfo
        self.lom = lom #List of DebugElementMemory

    def __str__(self):
        loe = self.loi + self.lom
        loe.sort(key=geti)
        strRep = ""
        for i in range(0,len(loe)):
            strRep += str(loe[i])
            strRep += "\n"
        return strRep

    def raw(self):
        loe = self.loi + self.lom
        loe.sort(key=geti)
        for i in range(0,len(loe)):
            loe[i] = str(loe[i])
        return loe

class DebugElementInfo:
    def __init__(self, info, i):
        self.info = info
        self.i = i

    def __str__(self):
        return ("READ IN: line " + str(self.i) + ", " + str(self.info))

class DebugElementMemory:
    def __init__(self, memory, i):
        self.memory = memory
        self.i = i

    def __str__(self):
        return ("MEMORY UPDATE: line  " + str(self.i) + ", " + str(self.memory))


def geti(loe):
    return loe.i
