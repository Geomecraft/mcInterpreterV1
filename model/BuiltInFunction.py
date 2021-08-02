import os
import json
from math import sqrt
from model.Memory import Memory
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

#built in function helpers

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
    interpreter.memory.currentNamespace = namespace
    if namespace in interpreter.memory.namespaces:
        pass
    else:
        #remember this namespace
        interpreter.memory.namespaces.append(namespace)

        #namespace  and namespace path creation
        os.mkdir(interpreter.memory.getCurrentNamespacePath())

        #subdirectories creation
        os.mkdir(interpreter.memory.getCurrentNamespacePath() + "/recipes")
        os.mkdir(interpreter.memory.getCurrentNamespacePath() + "/functions")
        os.mkdir(interpreter.memory.getCurrentNamespacePath() + "/predicates")
        os.mkdir(interpreter.memory.getCurrentNamespacePath() + "/item_modifiers")

        #add on load and tick function for this namespace
        with open(interpreter.memory.dataPackName + "/data/minecraft/tags/functions/load.json", 'r') as infile:
            loadData = json.loads(infile.read())
            loadData["values"].append(namespace + ":load")
        with open(interpreter.memory.dataPackName + "/data/minecraft/tags/functions/load.json", 'w') as outfile:
            json.dump(loadData, outfile, indent=INDENT)
        with open(interpreter.memory.getCurrentNamespacePath() + "/functions/load.mcfunction", 'w') as outfile:
            outfile.write("")

        with open(interpreter.memory.dataPackName + "/data/minecraft/tags/functions/tick.json", 'r') as infile:
            tickData = json.loads(infile.read())
            tickData["values"].append(namespace + ":tick")
        with open(interpreter.memory.dataPackName + "/data/minecraft/tags/functions/tick.json", 'w') as outfile:
            json.dump(tickData, outfile, indent=INDENT)
        with open(interpreter.memory.getCurrentNamespacePath() + "/functions/tick.mcfunction", 'w') as outfile:
            outfile.write("")

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

def onLoad(interpreter, *commands):
    with open(interpreter.memory.getCurrentNamespacePath() + "/functions/load.mcfunction", 'a') as outfile:
        for x in commands:
            outfile.write(x + "\n")
BuiltInFunctionsDict["onLoad"] = onLoad

def onTick(interpreter, *commands):
    with open(interpreter.memory.getCurrentNamespacePath() + "/functions/tick.mcfunction", 'a') as outfile:
        for x in commands:
            outfile.write(x + "\n")
BuiltInFunctionsDict["onTick"] = onTick

def onLandSnowball(interpreter, tag, *commands):
    if not interpreter.memory.flags.onLandSnowball:
        setCurrentNamespace(interpreter,"sys_0_snowball")
        functionPath = interpreter.memory.getCurrentNamespacePath() + "/functions/"
        with open(functionPath + "init.mcfunction", 'w') as outfile:
            outfile.write("scoreboard objectives add visfix dummy\n"
                          "scoreboard players set .-1 visfix -1\n"
                          "scoreboard players set .global visfix 1")
        with open(functionPath + "vis_fix.mcfunction", 'w') as outfile:
            outfile.write("execute if score .global visfix matches -1 run data modify entity @s Air set value 0s\n"
                          "execute if score .global visfix matches 1 run data modify entity @s Air set value 1s")
        onLoad(interpreter, "function sys_0_snowball:init")
        onTick(interpreter, "scoreboard players operation .global visfix *= .-1 visfix")

    index = str(interpreter.memory.sysIndex)
    setCurrentNamespace(interpreter,"sys_" + index + "_snowball")
    functionPath = interpreter.memory.getCurrentNamespacePath() + "/functions/"
    with open(functionPath + "found_ball.mcfunction", 'w') as outfile:
        outfile.write("summon snowball ~ ~ ~ {Tags:[\"" + tag + "\",\"init\"],Passengers:[{id:\"minecraft:area_effect_cloud\",Age:-2147483648,Duration:-1,WaitTime:-2147483648,Tags:[\"sys_spitem_" + index + "\"]}]}\n"
                      "data modify entity @e[type=snowball,tag=" + tag + ",tag=init,limit=1] Owner set from entity @s Owner\n"
                      "data modify entity @e[type=snowball,tag=" + tag + ",tag=init,limit=1] Motion set from entity @s Motion\n"
                      "tag @e[type=snowball,tag=" + tag + ",tag=init,limit=1] remove init\n"
                      "kill @s")
    with open(functionPath + "landed.mcfunction",'w') as outfile:
        outfile.write("kill @s\n")
    with open(functionPath + "landed.mcfunction",'a') as outfile:
        for x in commands:
            outfile.write(x + "\n")
    with open(functionPath + "main.mcfunction",'w') as outfile:
        outfile.write("execute as @e[type=snowball,tag=!" + tag + ",nbt={Item:{tag:{" + tag + ":1b}}}] at @s run function " + interpreter.memory.currentNamespace + ":found_ball\n"
                      "execute as @e[type=area_effect_cloud,tag=sys_spitem_" + index + "] unless predicate "+ interpreter.memory.currentNamespace + ":is_riding_snowball at @s run function " + interpreter.memory.currentNamespace + ":landed\n"
                      "execute as @e[type=snowball,tag=" + tag + "] run function sys_0_snowball:vis_fix\n")
    onTick(interpreter, "function " + interpreter.memory.currentNamespace + ":main")
    with open(interpreter.memory.getCurrentNamespacePath() + "/predicates/" + "is_riding_snowball.json",'w') as outfile:
        data = {"condition": "minecraft:entity_properties",
                "entity": "this",
                "predicate": {
                    "vehicle": {
                        "type": "minecraft:snowball",
                        "nbt": "{Tags:[\""+ tag +"\"]}"
                    }
                }}
        json.dump(data, outfile, indent=INDENT)
    interpreter.memory.sysIndex += 1
    interpreter.memory.flags.onLandSnowball = True
BuiltInFunctionsDict["onLand"] = onLandSnowball