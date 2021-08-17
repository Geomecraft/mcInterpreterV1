import os
import json
from math import sqrt


from model.General import assertExistNamespace, stripEachItem
from model.Parser import parseList, parseFunctionUsage
import model


class BuiltInFunction:
    def __init__(self, name = ""):
        self.name = name
        

#path stuff
# path = os.getcwd()
# print("Current working directory is " + '\033[94m' + path + '\033[0m')
INDENT = 4
GlobalBuiltInFunctionsDict = {}
LocalBuiltInFunctionsDict = {}

SYS_CUSTOM_RECIPE = "sys_custom_recipe"
RESTRICT_CRAFTING_DISPATCH_FN_NAME_SUFFIX = "_restrict_dispatch"
SYS_RIGHT_CLICK_DETECTION = "sys_right_click_detection"

#built in function helpers
def registerAsGlobal(function,name):
    GlobalBuiltInFunctionsDict[name] = function

def registerAsLocal(function, name):
    LocalBuiltInFunctionsDict[name] = function


#Actual functions
def Manifest(interpreter, name, formatNum, description):
    memory = interpreter.memory
    #pack folder and mcmeta
    os.makedirs(name + "/data")
    data = {"pack":{"pack_format": int(formatNum), "description": description}}
    with open(name + "/pack.mcmeta", 'w') as outfile:
        json.dump(data, outfile, indent=INDENT)
    memory.dataPackName = name

    #create default minecraft namespace
    os.mkdir(name + "/data/minecraft")
    os.makedirs(name + "/data/minecraft/tags/functions")

    #create load and tick
    with open(memory.dataPackName + "/data/minecraft/tags/functions/load.json", 'w') as outfile:
        json.dump({"values":[]}, outfile, indent=INDENT)
    with open(memory.dataPackName + "/data/minecraft/tags/functions/tick.json", 'w') as outfile:
        json.dump({"values":[]}, outfile, indent=INDENT)

    return "Datapack Manifestation Succesful"
GlobalBuiltInFunctionsDict["Manifest"] = Manifest

def setCurrentNamespace(interpreter,namespace):
    memory = interpreter.memory
    memory.currentNamespace = namespace
    if namespace in memory.namespaces:
        pass
    else:
        #remember this namespace
        memory.namespaces.append(namespace)

        #namespace  and namespace path creation
        os.mkdir(memory.getCurrentNamespacePath())

        #subdirectories creation
        os.mkdir(memory.getCurrentNamespacePath() + "/recipes")
        os.mkdir(memory.getCurrentNamespacePath() + "/functions")
        os.mkdir(memory.getCurrentNamespacePath() + "/advancements")
        os.mkdir(memory.getCurrentNamespacePath() + "/predicates")
        os.mkdir(memory.getCurrentNamespacePath() + "/item_modifiers")


        #add on load and tick function for this namespace
        with open(memory.dataPackName + "/data/minecraft/tags/functions/load.json", 'r') as infile:
            loadData = json.loads(infile.read())
            loadData["values"].append(namespace + ":load")
        with open(memory.dataPackName + "/data/minecraft/tags/functions/load.json", 'w') as outfile:
            json.dump(loadData, outfile, indent=INDENT)
        with open(memory.getCurrentNamespacePath() + "/functions/load.mcfunction", 'w') as outfile:
            outfile.write("")

        with open(memory.dataPackName + "/data/minecraft/tags/functions/tick.json", 'r') as infile:
            tickData = json.loads(infile.read())
            tickData["values"].append(namespace + ":tick")
        with open(memory.dataPackName + "/data/minecraft/tags/functions/tick.json", 'w') as outfile:
            json.dump(tickData, outfile, indent=INDENT)
        with open(memory.getCurrentNamespacePath() + "/functions/tick.mcfunction", 'w') as outfile:
            outfile.write("")

        # add root advancement for this datapack
        createAdvancement(interpreter, "root", {
            "criteria": {
                "Start": {
                    "trigger": "minecraft:tick"
                }
            },
            "requirements": [
                [
                    "Start"
                ]
            ]
        })

GlobalBuiltInFunctionsDict["namespace.set"] = setCurrentNamespace

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
GlobalBuiltInFunctionsDict["recipe.shaped"] = recipeCraftingShaped

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
GlobalBuiltInFunctionsDict["recipe.shapeless"] = recipeCraftingShapeless

def itemModifierSetNBT(interpreter, name, target, value):
    modifier = {"function":"minecraft:set_nbt",
                target:value}
    with open(interpreter.memory.getCurrentNamespacePath() + "/item_modifiers/" + name + ".json", 'w') as outfile:
        json.dump(modifier, outfile, indent=INDENT)
GlobalBuiltInFunctionsDict["item.modifier.setNBT"] = itemModifierSetNBT

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
GlobalBuiltInFunctionsDict["item.modifier.copyNBT"] = itemModifierCopyNBT

def onLoad(interpreter, *commands):
    with open(interpreter.memory.getCurrentNamespacePath() + "/functions/load.mcfunction", 'a') as outfile:
        for x in commands:
            outfile.write(x + "\n")
GlobalBuiltInFunctionsDict["onLoad"] = onLoad

def onTick(interpreter, *commands):
    with open(interpreter.memory.getCurrentNamespacePath() + "/functions/tick.mcfunction", 'a') as outfile:
        for x in commands:
            outfile.write(x + "\n")
GlobalBuiltInFunctionsDict["onTick"] = onTick

def onLandSnowball(interpreter, tag, *commands):
    memory = interpreter.memory
    originalNamespace = memory.currentNamespace
    #namespace for functionality only need to set once
    if not memory.flags.onLandSnowball:
        setCurrentNamespace(interpreter,"sys_0_snowball")
        functionPath = memory.getCurrentNamespacePath() + "/functions/"
        with open(functionPath + "init.mcfunction", 'w') as outfile:
            outfile.write("scoreboard objectives add visfix dummy\n"
                          "scoreboard players set .-1 visfix -1\n"
                          "scoreboard players set .global visfix 1")
        with open(functionPath + "vis_fix.mcfunction", 'w') as outfile:
            outfile.write("execute if score .global visfix matches -1 run data modify entity @s Air set value 0s\n"
                          "execute if score .global visfix matches 1 run data modify entity @s Air set value 1s")
        onLoad(interpreter, "function sys_0_snowball:init")
        onTick(interpreter, "scoreboard players operation .global visfix *= .-1 visfix")

    #namespcae for functionality need to individually tweaked for each different landing snow ball with different tags
    index = str(memory.sysIndex)
    setCurrentNamespace(interpreter,"sys_" + index + "_snowball")
    functionPath = memory.getCurrentNamespacePath() + "/functions/"
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
        outfile.write("execute as @e[type=snowball,tag=!" + tag + ",nbt={Item:{tag:{" + tag + ":1b}}}] at @s run function " + memory.currentNamespace + ":found_ball\n"
                      "execute as @e[type=area_effect_cloud,tag=sys_spitem_" + index + "] unless predicate " + memory.currentNamespace + ":is_riding_snowball at @s run function " + memory.currentNamespace + ":landed\n"
                      "execute as @e[type=snowball,tag=" + tag + "] run function sys_0_snowball:vis_fix\n")
    onTick(interpreter, "function " + memory.currentNamespace + ":main")
    with open(memory.getCurrentNamespacePath() + "/predicates/" + "is_riding_snowball.json", 'w') as outfile:
        data = {"condition": "minecraft:entity_properties",
                "entity": "this",
                "predicate": {
                    "vehicle": {
                        "type": "minecraft:snowball",
                        "nbt": "{Tags:[\""+ tag +"\"]}"
                    }
                }}
        json.dump(data, outfile, indent=INDENT)
    memory.sysIndex += 1
    memory.flags.onLandSnowball = True
    setCurrentNamespace(interpreter,originalNamespace)
GlobalBuiltInFunctionsDict["onLand"] = onLandSnowball

def forEach(interpreter, fn, var, collection, abstractBody):
    collectionlst = parseList(collection)
    if model.Syntax.FUNCTION_USAGE_SYNTAX.fullmatch(abstractBody): #abstract function #TODO, functionality not yet tested
        fnName = parseFunctionUsage(abstractBody)[0]
        fnlop = parseFunctionUsage(abstractBody)[1]
        for x in collectionlst:
            for i in range(0,len(fnlop)): #substitue collection item in place of var
                if fnlop[i] == var:
                    fnlop[i] = x
            fn.definition += interpreter.memory.function[fnName].useAbstractFn(fnlop) #use abstract function
    else: #abstract command
        for x in collectionlst:
            fn.definition.append(abstractBody.replace("<" + var + ">", x))
LocalBuiltInFunctionsDict["for.each"] = forEach

def forEachGlobal(interpreter, var, collection, globalFunctionCall):
    collectionlst = parseList(collection)
    #TODO, refactor interpreter so it no longer deals with file input and only with interpreting,
    # and then use the power of interpreter to interpret whatever is inputed in forEachGlobal.
    # Details such as how to handle line number and stuff need to be thought out
    # if FUNCTION_USAGE_SYNTAX.fullmatch(abstractBody): #abstract function
    #     pass
    # else: #abstract command
    #     for x in collectionlst:
    #         fn.definition.append(abstractBody.replace("<" + var + ">", x))



def loop(interpreter, fn, interval = "1t", executeIfClause = ""):
    waitThenExecuteFunction(interpreter, fn, interval, fn.name, executeIfClause)
LocalBuiltInFunctionsDict["loop"] = loop

def breakMcFunction(interpreter, fn, mcFunction, executeIfClause =""):
    if executeIfClause[-3:] != "run" and executeIfClause != "":
        executeIfClause += " run "
    fn.definition.append(executeIfClause + "schedule clear " + mcFunction)
LocalBuiltInFunctionsDict["break"] = breakMcFunction

def waitThenExecuteFunction(interpreter, fn, waitTime, mcFunction, executeIfClause = ""):
    if executeIfClause[-3:] != "run" and executeIfClause != "":
        executeIfClause += " run "
    fn.definition.append(executeIfClause + "schedule function " + mcFunction + " " + waitTime + " append")
LocalBuiltInFunctionsDict["wait"] = waitThenExecuteFunction

#These two functions schedule functions wait time in replace mode, which means later schedule replaces the old one, they also cannot be break
def loopPreserveExecutor(interpreter, fn, interval = "1t", executeIfClause = ""):
    waitThenExecuteFunctionPreserveExecutor(interpreter, fn, interval, fn.name, executeIfClause)
LocalBuiltInFunctionsDict["loop.preserve.executor"] = loopPreserveExecutor
def waitThenExecuteFunctionPreserveExecutor(interpreter, fn, waitTime, mcFunction, executeIfClause = ""):
    if executeIfClause[-3:] != "run" and executeIfClause != "":
        executeIfClause += " run "
    def getWaitTimeInTickScore(rawWaitTime):
        if rawWaitTime[-1] == "t":
            return str(int(rawWaitTime[:-1]) + 1)
        elif rawWaitTime[-1] == "s":
            return str(int(rawWaitTime[:-1]) * 20 + 1)
        elif rawWaitTime[-1] == "d":
            return str(int(rawWaitTime[:-1]) * 24000 + 1)
    waitTimeInTickScore = getWaitTimeInTickScore(waitTime)
    def getSysIdString(interpreter):
        return "sys_id_" + interpreter.memory.getIndex()
    onLoad(interpreter, "scoreboard objectives add " + getSysIdString(interpreter) + " dummy")
    fn.definition.append(executeIfClause + "scoreboard players set @s " + getSysIdString(interpreter) + " 1")
    onTick(interpreter, "execute as @a[scores={" + getSysIdString(interpreter) + "=1..}] run scoreboard players add @s " + getSysIdString(interpreter) + " 1",
           "execute as @a[scores={" + getSysIdString(interpreter) + "=" + waitTimeInTickScore + "}] run function " + mcFunction,
           "execute as @a[scores={" + getSysIdString(interpreter) + "=" + waitTimeInTickScore + "}] run scoreboard players set @s " + getSysIdString(interpreter) + " 0")
    interpreter.memory.increment()
LocalBuiltInFunctionsDict["wait.preserve.executor"] = waitThenExecuteFunctionPreserveExecutor

def breakAll(interpreter,fn):
    allfn = interpreter.memory.function.keys()
    for x in allfn:
        fn.definition.append("schedule clear " + x)
    for i in range(0, interpreter.memory.sysIndex):
        fn.definition.append("scoreboard players set @a sys_id_" + str(i) + " 0")
LocalBuiltInFunctionsDict["break.all"] = breakAll

def recipeCustomRestrictPlayer(interpreter, customCraftingRecipeName, selectorArguments):
    preserveNameSpace(interpreter)

    setCurrentNamespace(interpreter, SYS_CUSTOM_RECIPE)
    fnstr = accessFunction(interpreter, customCraftingRecipeName + RESTRICT_CRAFTING_DISPATCH_FN_NAME_SUFFIX)
    fnstr = fnstr.replace("@s[]", "@s" + selectorArguments)
    createFunction(interpreter,customCraftingRecipeName + RESTRICT_CRAFTING_DISPATCH_FN_NAME_SUFFIX,fnstr)

    revertNameSpace(interpreter)
registerAsGlobal(recipeCustomRestrictPlayer, "recipe.custom.restrict")

def recipeCraftingShapedCustom(interpreter, recipeName, result, count, *loa):
    preserveNameSpace(interpreter)

    setCurrentNamespace(interpreter, SYS_CUSTOM_RECIPE)
    recipeCraftingShaped(interpreter, recipeName, "minecraft:knowledge_book", 1,  *loa)
    createFunction(interpreter, recipeName,
                   "give @s " + result + " " + count,
                   "clear @s minecraft:knowledge_book")
    createFunction(interpreter, recipeName + RESTRICT_CRAFTING_DISPATCH_FN_NAME_SUFFIX,
                   "execute as @s[] run function " + SYS_CUSTOM_RECIPE + ":" + recipeName,
                   "recipe take @s " + SYS_CUSTOM_RECIPE + ":" + recipeName,
                   "advancement revoke @s only " + SYS_CUSTOM_RECIPE + ":" + recipeName,)
    advData = {
        "criteria": {
            recipeName: {
                "trigger": "minecraft:recipe_unlocked",
                "conditions": {
                    "recipe": SYS_CUSTOM_RECIPE + ":" + recipeName
                }
            }
        },
        "requirements": [
            [
                recipeName
            ]
        ],
        "rewards": {
            "function": SYS_CUSTOM_RECIPE + ":" + recipeName + RESTRICT_CRAFTING_DISPATCH_FN_NAME_SUFFIX
        },
        "parent": SYS_CUSTOM_RECIPE + ":root"
    }
    createAdvancement(interpreter, recipeName, advData)
    revertNameSpace(interpreter)
registerAsGlobal(recipeCraftingShapedCustom, "recipe.custom.shaped")

def recipeCraftingShapelessCustom(interpreter, recipeName, result, count, *loa):
    preserveNameSpace(interpreter)

    setCurrentNamespace(interpreter, SYS_CUSTOM_RECIPE)
    recipeCraftingShapeless(interpreter, recipeName, "minecraft:knowledge_book", 1,  *loa)
    createFunction(interpreter, recipeName,
                   "give @s " + result + " " + count,
                   "clear @s minecraft:knowledge_book")
    createFunction(interpreter, recipeName + RESTRICT_CRAFTING_DISPATCH_FN_NAME_SUFFIX,
                   "execute as @s[] run function " + SYS_CUSTOM_RECIPE + ":" + recipeName,
                   "recipe take @s " + SYS_CUSTOM_RECIPE + ":" + recipeName,
                   "advancement revoke @s only " + SYS_CUSTOM_RECIPE + ":" + recipeName,)
    advData = {
        "criteria": {
            recipeName: {
                "trigger": "minecraft:recipe_unlocked",
                "conditions": {
                    "recipe": SYS_CUSTOM_RECIPE + ":" + recipeName
                }
            }
        },
        "requirements": [
            [
                recipeName
            ]
        ],
        "rewards": {
            "function": SYS_CUSTOM_RECIPE + ":" + recipeName + RESTRICT_CRAFTING_DISPATCH_FN_NAME_SUFFIX
        },
        "parent": SYS_CUSTOM_RECIPE + ":root"
    }
    createAdvancement(interpreter, recipeName, advData)
    revertNameSpace(interpreter)
registerAsGlobal(recipeCraftingShapelessCustom, "recipe.custom.shapeless")

def onRightClick(interpreter, carrotOnAStickTag, *commands):
    preserveNameSpace(interpreter)

    memory = interpreter.memory
    setCurrentNamespace(interpreter, SYS_RIGHT_CLICK_DETECTION)
    if not memory.flags.onRightClick:
        onLoad(interpreter, "scoreboard objectives add carrot_click minecraft.used:minecraft.carrot_on_a_stick")

    ontick = accessFunction(interpreter, "tick")
    ontick = ontick.replace("execute as @a[scores={carrot_click=1..}] at @s run scoreboard players set @s carrot_click 0", "")
    createFunction(interpreter, "tick", ontick)

    createFunction(interpreter, SYS_RIGHT_CLICK_DETECTION + "_" + memory.getIndex(), *commands)
    onTick(interpreter, "execute as @a[scores={carrot_click=1..}, nbt={SelectedItem:{tag:{" + carrotOnAStickTag + ":1b}}}] at @s run function " + SYS_RIGHT_CLICK_DETECTION + ":" + SYS_RIGHT_CLICK_DETECTION + "_" + memory.getIndex(),
           "execute as @a[scores={carrot_click=1..}] at @s run scoreboard players set @s carrot_click 0")

    memory.increment()
    revertNameSpace(interpreter)
registerAsGlobal(onRightClick, "onClick.right")

def importAdvancment(interpreter, advancementFilePath, advancementName = None):
    if advancementName == None:
        advancementName = advancementFilePath
    advdict = json.loads(interpreter.fetchFromInput(advancementFilePath))
    createAdvancement(interpreter, advancementName, advdict)
registerAsGlobal(importAdvancment, "import.adv")

def importItemModifier(interpreter, itemModifierFilePath, itemModifierName = None):
    if itemModifierName == None:
        itemModifierName = itemModifierFilePath
    itemdict = json.loads(interpreter.fetchFromInput(itemModifierFilePath))
    createItemModifier(interpreter, itemModifierName, itemdict)
registerAsGlobal(importItemModifier, "import.item.modifier")

def createFunction(interpreter, functionName, *FunctionBody):
    with open(interpreter.memory.getCurrentNamespacePath() + "/functions/" + functionName + ".mcfunction",'w') as outfile:
        str = ""
        for x in FunctionBody:
            str += x
            str += "\n"
        outfile.write(str)

def accessFunction(interpreter, functionName):
    with open(interpreter.memory.getCurrentNamespacePath() + "/functions/" + functionName + ".mcfunction",'r') as infile:
        return infile.read()

def createAdvancement(interpreter, advancementName, dict):
    with open(interpreter.memory.getCurrentNamespacePath() + "/advancements/" + advancementName + ".json",'w') as outfile:
        json.dump(dict, outfile, indent=INDENT)

def createItemModifier(interpreter, itemModifierName, itemdict):
    with open(interpreter.memory.getCurrentNamespacePath() + "/item_modifiers/" + itemModifierName + ".json",'w') as outfile:
        json.dump(itemdict, outfile, indent=INDENT)

def preserveNameSpace(interpreter):
    interpreter.memory.tempNamespace = interpreter.memory.currentNamespace

def revertNameSpace(interpreter):
    setCurrentNamespace(interpreter, interpreter.memory.tempNamespace)
