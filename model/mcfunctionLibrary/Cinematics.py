#This package requires the latest version of the carpet mod, specifically, the /player commands

from model.mcfunctionLibrary.BuiltInFunction import onTick, onLoad
import model

INDENT = 4
SYS_PLAYER_SCORE_PREFIX = "sys_player_"

GlobalBuiltInFunctionsDict = {}
LocalBuiltInFunctionsDict = {}
#built in function helpers
def registerAsGlobal(function,name):
    GlobalBuiltInFunctionsDict[name] = function

def registerAsLocal(function, name):
    LocalBuiltInFunctionsDict[name] = function

def cinematics(interpreter):
    pass

def freeze(interpreter, fn, player): #stop all this player's actions
    fn.appendDefinition("player " + player + " stop",
                        "attribute " + player + " minecraft:generic.movement_speed base set 0")
    for i in range(0,interpreter.memory.sysIndexMax):
        sys_score = SYS_PLAYER_SCORE_PREFIX + str(i)
        fn.appendDefinition("execute as @a[scores={" + sys_score + "=1}] run scoreboard players set @s " + sys_score + " 0")
registerAsLocal(freeze, "cin.freeze")

def unfreeze(interpreter, fn, player):
    fn.appendDefinition("attribute " + player + " minecraft:generic.movement_speed base set 0.1")
registerAsLocal(unfreeze, "cin.unfreeze")

# fn.appendDefinition(
#     "execute at " + player + " run summon area_effect_cloud " + target + " {Duration:72000,Tags:[\"" + sys_tag + "\"]}")
# fn.appendDefinition(
#     "execute at @e[type=minecraft:area_effect_cloud, nbt={Tags:[" + sys_tag + "]}] run player " + player + " look at " + target)
# interpreter.memory.sysIndex += 1

def cinStaticFace(interpreter, fn, player, target):
    freeze(interpreter, fn, player)
    if model.Syntax.isCoordinate(target): #target is a coordinate
        fn.appendDefinition("execute at " + player + " run player " + player + " look at " + target)
    else: #target is a player name or selector
        fn.appendDefinition("execute at " + target + " run player " + player + " look at ~ ~1.5 ~")
registerAsLocal(cinStaticFace, "cin.static.face")


def cinDynamicFace(interpreter, fn, player, target):
    freeze(interpreter, fn, player)
    sys_score = SYS_PLAYER_SCORE_PREFIX + interpreter.memory.getIndex()
    onLoad(interpreter, "scoreboard objectives add " + sys_score + " dummy")
    if model.Syntax.isCoordinate(target): #target is a coordinate
        onTick(interpreter, "execute at " + player + " if score " + player + " " + sys_score + " matches 1 run player " + player + " look at " + target)
    else: #target is a player name or selector
        onTick(interpreter, "execute at " + player + " run execute at " + target + " if score " + player + " " + sys_score + " matches 1 run player " + player + " look at ~ ~1.5 ~")
    fn.appendDefinition("scoreboard players set " + player + " " + sys_score + " 1")
    interpreter.memory.sysIndex += 1
registerAsLocal(cinDynamicFace, "cin.dynamic.face")

def cinStaticWalk(interpreter,fn, player, target):
    cinStaticFace(interpreter, fn, player, target)
    fn.appendDefinition("player " + player + " move forward")
    if model.Syntax.isCoordinate(target): #target is a coordinate
        onTick(interpreter, "execute at " + player + " if score " + player + " " + sys_score + " matches 1 run player " + player + " look at " + target)
    else: #target is a player name or selector
        onTick(interpreter, "execute at " + player + " run execute at " + target + " if score " + player + " " + sys_score + " matches 1 run player " + player + " look at ~ ~1.5 ~")
registerAsLocal(cinStaticWalk, "cin.static.walk")

def cinDynamicWalk(interpreter,fn, player, target):
    cinDynamicFace(interpreter, fn, player, target)
    fn.appendDefinition("player " + player + " move forward")
registerAsLocal(cinStaticWalk, "cin.static.walk")

# def registerThisLibrary():
#     GlobalBuiltInFunctionsDict.update(LocalBuiltInFunctionsDict)
#     LibraryDict["Cinematics"] = GlobalBuiltInFunctionsDict
# registerThisLibrary()
