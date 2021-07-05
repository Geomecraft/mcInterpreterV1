import os
import json
from math import sqrt

from model.Exceptions import IncorrectArguments, NamespaceError


class BuiltInFunction:
    def __init__(self, name = ""):
        self.name = name
        

#path stuff
# path = os.getcwd()
# print("Current working directory is " + '\033[94m' + path + '\033[0m')
LETTERS_FOR_RECIPE = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
INDENT = 4
BuiltInFunctionsDict = {}



#Assert preconditions
def assertExistNamespace(memory):
    try:
        memory.currentNamespace
    except: #what error?
        raise NamespaceError("no current namespace is set")



#Actual functions
def Manifest(interpreter, name, formatNum, description):
    #pack folder and mcmeta
    os.makedirs(name + "/data")
    data = {"pack":{"pack_format": int(formatNum), "description": description}}
    with open(name + "/pack.mcmeta", 'w') as outfile:
        json.dump(data, outfile, indent=INDENT)
    interpreter.memory.dataPackName = name

    #create default minecraft namespace
    os.mkdir(name + "/data/minecraft")

    return "Datapack Manifestation Succesful"
BuiltInFunctionsDict["Manifest"] = Manifest

def setCurrentNamespace(interpreter,namespace):
    #namespace  and namespace path creation
    interpreter.memory.currentNamespace = namespace
    os.mkdir(interpreter.memory.getCurrentNamespacePath())

    #subdirectories creation
    os.mkdir(interpreter.memory.getCurrentNamespacePath() + "/recipes")
    os.mkdir(interpreter.memory.getCurrentNamespacePath() + "/functions")
BuiltInFunctionsDict["namespace.set"] = setCurrentNamespace

def recipeCraftingShaped(interpreter,*loa):
    assertExistNamespace(interpreter.memory)

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

    with open(interpreter.memory.getCurrentNamespacePath() + "/recipes/" + loa[0] + ".json", 'w') as outfile:
        json.dump(data, outfile, indent=INDENT)
BuiltInFunctionsDict["recipe.shaped"] = recipeCraftingShaped

def recipeCraftingShapeless(interpreter,*loa):
    assertExistNamespace(interpreter.memory)

    loi = []
    for i in range(3,len(loa)):
        loi.append({"item":loa[i]})

    data = {
        "type":"minecraft:crafting_shapeless",
        "ingredients":loi,
        "result": {"item": loa[1],
                   "count": int(loa[2])}
    }

    with open(interpreter.memory.getCurrentNamespacePath() + "/recipes/" + loa[0] + ".json", 'w') as outfile:
        json.dump(data, outfile, indent=INDENT)
BuiltInFunctionsDict["recipe.shapeless"] = recipeCraftingShapeless

