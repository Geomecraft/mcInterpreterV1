import os
import json
from math import sqrt

from model.Exceptions import IncorrectArguments, NamespaceError


#path stuff
# path = os.getcwd()
# print("Current working directory is " + '\033[94m' + path + '\033[0m')
LETTERS_FOR_RECIPE = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
INDENT = 4

#Check parameter numbers

#accepts a number
def assertRightNumOfParameter(loa, n):
    if (len(loa) != n):
        raise IncorrectArguments("expected " + str(n) + " arguments, got " + str(len(loa)) + " arguments instead")

#accepts a list of numbers or range (such as [1,3] representing 1 to 3 parameters)
def assertRightNumOfParameterMultiple(loa, loi):
    for i in range(0, len(loi)):
        if isinstance(loi[i],int): #number
            if (len(loa) == loi[i]):
                return
        else: #range
            if (loi[i][0] <= len(loa) <= loi[i][1]):
                return

    ns = ""
    if len(loi) == 1: #just a range or a number
        if isinstance(loi[-1], int):  # number
            ns += str(loi[-1])
        else:
            ns += str(loi[-1][0]) + "-" + str(loi[-1][1])
    else: #algorithm for multiple, has the "or"
        for i in range(0, len(loi) - 1):
            if isinstance(loi[i],int): #number
                ns += str(loi[i])
                ns += ", "
            else: #range
                ns += str(loi[i][0]) + "-" + str(loi[i][1]) + ", "
        if isinstance(loi[-1],int): #number
            ns += "or " + str(loi[-1])
        else:
            ns += "or" + str(loi[-1][0]) + "-" + str(loi[-1][1])
    raise IncorrectArguments("expected " + ns + " arguments, got " + str(len(loa)) + " arguments instead")



#Assert existance of namespace
def assertExistNamespace(memory):
    try:
        memory["current namespace"]
    except: #what error?
        raise NamespaceError("no current namespace is set")


#Assert types

def assertInt(a):
    try:
        int(a)
    except ValueError:
        raise IncorrectArguments("expected int type, got string instead")



#Actual functions
def Manifest(loa, memory):
    assertRightNumOfParameter(loa, 3)

    name = loa[0]
    formatNum = loa[1]
    description = loa[2]

    assertInt(formatNum)

    #pack folder and mcmeta
    os.makedirs(name + "/data")
    data = {"pack":{"pack_format": int(formatNum), "description": description}}
    with open(name + "/pack.mcmeta", 'w') as outfile:
        json.dump(data, outfile, indent=INDENT)
    memory["datapack name"] = name

    #create default minecraft namespace
    os.mkdir(name + "/data/minecraft")

    return "Datapack Manifestation Succesful"

def setCurrentNamespace(loa,memory):
    assertRightNumOfParameter(loa, 1)

    #namespace  and namespace path creation
    memory["current namespace"] = loa[0]
    memory["namespace path"] = memory["datapack name"] + "/data/" + memory["current namespace"]
    os.mkdir(memory["namespace path"])

    #subdirectories creation
    os.mkdir(memory["namespace path"] + "/recipes")
    os.mkdir(memory["namespace path"] + "/functions")

def recipeCraftingShaped(loa, memory):

    assertRightNumOfParameterMultiple(loa, [7,12])
    assertExistNamespace(memory)
    assertInt(loa[2])

    patternRaw = []
    key = {}
    for i in range(3,len(loa)):
        if loa[i] == "empty":
            patternRaw.append(" ")
        else:
            patternRaw.append(LETTERS_FOR_RECIPE[i-3])
            key[LETTERS_FOR_RECIPE[i-3]] = {"item":loa[i]}

    pattern = []
    tempString = ""
    for i in range(0,len(patternRaw)):
        tempString += patternRaw[i]
        if ((i+1) % int(sqrt(len(patternRaw)))) == 0:
            pattern.append(tempString)
            tempString = ""

    data = {"type":"minecraft:crafting_shaped",
            "pattern": pattern,
            "key":key,
            "result":{"item":loa[1],
                      "count":int(loa[2])}}

    with open(memory["namespace path"] + "/recipes/" + loa[0] + ".json", 'w') as outfile:
        json.dump(data, outfile, indent=INDENT)

def recipeCraftingShapeless(loa,memory):
    assertRightNumOfParameterMultiple(loa,[[4,12]])
    assertInt(loa[2])

    loi = []
    for i in range(3,len(loa)):
        loi.append({"item":loa[i]})

    data = {
        "type":"minecraft:crafting_shapeless",
        "ingredients":loi,
        "result": {"item": loa[1],
                   "count": int(loa[2])}
    }

    with open(memory["namespace path"] + "/recipes/" + loa[0] + ".json", 'w') as outfile:
        json.dump(data, outfile, indent=INDENT)




#Actual dictionary
BuiltInFunctionsDict = {
    "Manifest":Manifest,
    "namespace.set":setCurrentNamespace,
    "recipe.shaped":recipeCraftingShaped,
    "recipe.shapeless":recipeCraftingShapeless
}

