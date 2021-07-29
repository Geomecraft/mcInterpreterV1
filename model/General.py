
import shutil
from os import listdir, path, unlink

from model.Exceptions import NamespaceError


def stripEachItem(lst):
    for i in range(0, len(lst)):
        lst[i] = lst[i].strip()  # get rid of spaces attached to parameters from splicing

def readFunctionUsage(fnstr):
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

    return fnName, fnlop

def assertExistNamespace(memory):
    try:
        memory.currentNamespace
    except: #what error?
        raise NamespaceError("no current namespace is set")

def clearDirectory(dirPath):
    for filename in listdir(dirPath):
        file_path = path.join(dirPath, filename)
        try:
            if path.isfile(file_path) or path.islink(file_path):
                unlink(file_path)
            elif path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))