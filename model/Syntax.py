import re

CONSTANT_DEFINITION_SYNTAX = re.compile(r".+=.+")
FUNCTION_DEFINITION_SYNTAX = re.compile(r"def\s+(abstract\s+)?(\S)+\(.*\)\s*{")
FUNCTION_USAGE_SYNTAX = re.compile(r"(\S)+\(.*")

# def constantIsCompletlyOnItsOwnAsAnArgumentInAFunctionCall(linestr, constantName):
#     if constantName not in linestr:
#         return False
#     elif:

