from model.FileManage import clearDirectory
from model.GlobalInterpreter import GlobalInterpreter
import os

#change path to mcInterpreterV1
# print(os.getcwd())
# parentPath = os.path.dirname(os.getcwd())
# os.chdir(parentPath)
# print(os.getcwd())

#helpers
from model.Options import Options


def assertException(testPath, exceptionMessage):
    try:
        GlobalInterpreter.interpretPath(testPath, True, False)
        assert (False)
    except Exception as e:
        assert (str(e) == exceptionMessage)



#before
clearDirectory("output")
def setupInterpreter():
    interpreter = GlobalInterpreter()
    interpreter.options = Options.constructFromJsonFile("option.json")
    return interpreter
#actual tests
def ManifestTest():
    interpreter = setupInterpreter()
    interpreter.options.mainFilePath = "ManifestTest"
    interpreter.interpretPath()
def NamespaceTest():
    interpreter = setupInterpreter()
    interpreter.options.mainFilePath = "NamespaceTest"
    interpreter.interpretPath()
def RecipeTest():
    interpreter = setupInterpreter()
    interpreter.options.mainFilePath = "RecipeTest"
    interpreter.interpretPath()
def DefineUserFunctionsTest():
    interpreter = setupInterpreter()
    interpreter.options.mainFilePath = "DefineUserFunctionsTest"
    interpreter.interpretPath()
def ConstantsTest():
    interpreter = setupInterpreter()
    interpreter.options.mainFilePath = "ConstantsTest"
    interpreter.interpretPath()
def LoopBreakAndWaitTest():
    interpreter = setupInterpreter()
    interpreter.options.mainFilePath = "LoopBreakAndWaitTest"
    interpreter.interpretPath()
def LoopWaitAndWaitPreserveExecutorTest():
    interpreter = setupInterpreter()
    interpreter.options.mainFilePath = ""
#Actual impelmenting stuff, run with caution
# ManifestTest()
# NamespaceTest()
# RecipeTest()
# LoadAndTickTest()
# DefineUserFunctionsTest()
# ConstantsTest()
# LoopBreakAndWaitTest()

