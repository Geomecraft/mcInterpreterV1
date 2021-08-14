from model.General import stripEachItem


def parseList(listasString):
    lst = listasString[1:-1].split(",")
    stripEachItem(lst)
    return lst


def parseFunctionUsage(fnstr):
    fnName = fnstr.split("(", 1)[0]
    lopstr = fnstr.split("(",1)[1].rsplit(")",1)[0]

    fnlop = []
    lastParseIndex = 0
    scope = 0
    ignore = False
    for i in range(0,len(lopstr)-1):
        if lopstr[i] == "," and not ignore:
            fnlop.append(lopstr[lastParseIndex:i])
            lastParseIndex = i + 1
        elif (lopstr[i] == "\"" and lopstr[i+1] == "<"):
            scope += 1
        elif (lopstr[i] == ">" and lopstr[i+1] == "\""):
            scope -= 1

        if scope > 0:
            ignore = True
        elif scope == 0:
            ignore = False
        else:
            pass
    fnlop.append(lopstr[lastParseIndex:len(lopstr)])

    #remove the most outer layer of "< and "> for each item, and strip them
    for i in range(0, len(fnlop)):
        fnlop[i] = fnlop[i].strip()
        if fnlop[i][0:2] == "\"<" and fnlop[i][-2:] == ">\"":
            fnlop[i] = fnlop[i][2:-2]

    #if no fnlop
    if fnlop == [""]:
        fnlop = []
    return fnName, fnlop