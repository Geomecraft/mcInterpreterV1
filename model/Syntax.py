import re

from model.mcfunctionLibrary.MasterLibrary import LocalBuiltInFunctionsDict, GlobalBuiltInFunctionsDict
from model.Parser import parseFunctionUsage

CONSTANT_DEFINITION_SYNTAX = re.compile(r".+=.+")
FUNCTION_DEFINITION_SYNTAX = re.compile(r"def\s+(abstract\s+)?(\S)+\(.*\)\s*{")
FUNCTION_USAGE_SYNTAX = re.compile(r"(\S)+\(.*")
MINECRAFT_COORDINATE_SYNTAX = re.compile(r"(([~^]-?[\d.]*)|(-?[\d.]+))\s(([~^]-?[\d.]*)|(-?[\d.]+))\s(([~^]-?[\d.]*)|(-?[\d.]+))")

# EFFECTS: see if this line of code is suppose to do X (for all isX function below)
def isComment(str):
    if str != "":
        return str[0] == "#"

def isConstantDefinition(str):
    return CONSTANT_DEFINITION_SYNTAX.fullmatch(str)

def isFunctionDefinition(str):
    return FUNCTION_DEFINITION_SYNTAX.fullmatch(str)

def isFunctionUsage(str):
    return FUNCTION_USAGE_SYNTAX.fullmatch(str)

def isGlobalBuiltInFunctionUsage(str):
    return isFunctionUsage and (parseFunctionUsage(str)[0] in GlobalBuiltInFunctionsDict)

def isLocalBuiltInFunctionUsage(str):
    return isFunctionUsage and (parseFunctionUsage(str)[0] in LocalBuiltInFunctionsDict)

def isSelector(str):
    return str[0] == "@"

def isValidPlayerName(str):
    return not (" " in str)

def isCoordinate(str):
    return MINECRAFT_COORDINATE_SYNTAX.fullmatch(str)


