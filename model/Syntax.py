import re

from model.BuiltInFunction import LocalBuiltInFunctionsDict, GlobalBuiltInFunctionsDict
from model.Parser import parseFunctionUsage

CONSTANT_DEFINITION_SYNTAX = re.compile(r".+=.+")
FUNCTION_DEFINITION_SYNTAX = re.compile(r"def\s+(abstract\s+)?(\S)+\(.*\)\s*{")
FUNCTION_USAGE_SYNTAX = re.compile(r"(\S)+\(.*")

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



