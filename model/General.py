def stripEachItem(lst):
    for i in range(0, len(lst)):
        lst[i] = lst[i].strip()  # get rid of spaces attached to parameters from splicing

def readFunctionUsage(fnstr):
    fnName = fnstr.split("(", 1)[0]
    fnlop = fnstr.split("(", 1)[1][:-1].split(",")
    return fnName, fnlop