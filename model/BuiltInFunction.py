import os
import json
from math import sqrt

from model.Exceptions import IncorrectArguments, NamespaceError
from model.General import assertExistNamespace


class BuiltInFunction:
    def __init__(self, name = ""):
        self.name = name
        

#path stuff
# path = os.getcwd()
# print("Current working directory is " + '\033[94m' + path + '\033[0m')
INDENT = 4
BuiltInFunctionsDict = {}

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
    os.makedirs(name + "/data/minecraft/tags/functions")

    #create load and tick
    with open(interpreter.memory.dataPackName + "/data/minecraft/tags/functions/load.json", 'w') as outfile:
        json.dump({"values":[]}, outfile, indent=INDENT)
    with open(interpreter.memory.dataPackName + "/data/minecraft/tags/functions/tick.json", 'w') as outfile:
        json.dump({"values":[]}, outfile, indent=INDENT)

    return "Datapack Manifestation Succesful"
BuiltInFunctionsDict["Manifest"] = Manifest

def setCurrentNamespace(interpreter,namespace):
    #namespace  and namespace path creation
    interpreter.memory.currentNamespace = namespace
    os.mkdir(interpreter.memory.getCurrentNamespacePath())

    #subdirectories creation
    os.mkdir(interpreter.memory.getCurrentNamespacePath() + "/recipes")
    os.mkdir(interpreter.memory.getCurrentNamespacePath() + "/functions")
    os.mkdir(interpreter.memory.getCurrentNamespacePath() + "/item_modifiers")

    #add on load and tick function for this namespace
    with open(interpreter.memory.dataPackName + "/data/minecraft/tags/functions/load.json", 'r') as infile:
        loadData = json.loads(infile.read())
        loadData["values"].append(namespace + ":load")
    with open(interpreter.memory.dataPackName + "/data/minecraft/tags/functions/load.json", 'w') as outfile:
        json.dump(loadData, outfile, indent=INDENT)
    with open(interpreter.memory.dataPackName + "/data/minecraft/tags/functions/tick.json", 'r') as infile:
        tickData = json.loads(infile.read())
        tickData["values"].append(namespace + ":tick")
    with open(interpreter.memory.dataPackName + "/data/minecraft/tags/functions/tick.json", 'w') as outfile:
        json.dump(tickData, outfile, indent=INDENT)

BuiltInFunctionsDict["namespace.set"] = setCurrentNamespace

def recipeCraftingShaped(interpreter,*loa):
    assertExistNamespace(interpreter.memory)

    LETTERS_FOR_RECIPE = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

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

def itemModifierSetNBT(interpreter, name, target, value):
    modifier = {"function":"minecraft:set_nbt",
                target:value}
    with open(interpreter.memory.getCurrentNamespacePath() + "/item_modifiers/" + name + ".json", 'w') as outfile:
        json.dump(modifier, outfile, indent=INDENT)
BuiltInFunctionsDict["item.modifier.setNBT"] = itemModifierSetNBT

#op, sourcePath, targetPath

def itemModifierCopyNBT(interpreter,name, sourceStorage,*loops):
    ops = []
    for i in range(0,len(loops),3):
        sourcePath = loops[i]
        targetPath = loops[i+1]
        operation = loops[i+2]
        ops.append({"source": sourcePath,
                    "target": targetPath,
                    "op": operation})

    modifier = {"function": "copy_nbt",
                "source": {
                    "type": "storage",
                    "source": sourceStorage
                },
                "ops": ops
                }
    with open(interpreter.memory.getCurrentNamespacePath() + "/item_modifiers/" + name + ".json", 'w') as outfile:
        json.dump(modifier, outfile, indent=INDENT)
BuiltInFunctionsDict["item.modifier.copyNBT"] = itemModifierCopyNBT
