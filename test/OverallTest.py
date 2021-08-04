from model.General import clearDirectory
from model.Interpreter import Interpreter
import os

#change path to mcInterpreterV1
# print(os.getcwd())
# parentPath = os.path.dirname(os.getcwd())
# os.chdir(parentPath)
# print(os.getcwd())

#helpers
def assertException(testPath, exceptionMessage):
    try:
        Interpreter.interpret(testPath, True, False)
        assert (False)
    except Exception as e:
        assert (str(e) == exceptionMessage)



#before
clearDirectory("output")
def setupInterpreter():
    interpreter = Interpreter()
    interpreter.options.datapackOutputPath = "output"
    return interpreter
#actual tests
def ManifestTest():
    interpreter = setupInterpreter()
    interpreter.interpret("ManifestTest")
def NamespaceTest():
    interpreter = setupInterpreter()
    interpreter.interpret("NamespaceTest")
def RecipeTest():
    interpreter = setupInterpreter()
    interpreter.interpret("RecipeTest")
def DefineUserFunctionsTest():
    interpreter = setupInterpreter()
    interpreter.interpret("DefineUserFunctionsTest")
def ConstantsTest():
    interpreter = setupInterpreter()
    interpreter.interpret("ConstantsTest")
def LoopBreakAndWaitTest():
    interpreter = setupInterpreter()
    interpreter.interpret("LoopBreakAndWaitTest")
#Actual impelmenting stuff, run with caution
# ManifestTest()
# NamespaceTest()
# RecipeTest()
# LoadAndTickTest()
# DefineUserFunctionsTest()
# ConstantsTest()
LoopBreakAndWaitTest()

