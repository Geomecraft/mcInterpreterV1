from model.FileManage import clearDirectory
from model.GlobalInterpreter import GlobalInterpreter
import os

#change path to mcInterpreterV1
# print(os.getcwd())
# parentPath = os.path.dirname(os.getcwd())
# os.chdir(parentPath)
# print(os.getcwd())

#helpers
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
    interpreter.options.datapackOutputPath = "output"
    return interpreter
#actual tests
def ManifestTest():
    interpreter = setupInterpreter()
    interpreter.interpretPath("ManifestTest")
def NamespaceTest():
    interpreter = setupInterpreter()
    interpreter.interpretPath("NamespaceTest")
def RecipeTest():
    interpreter = setupInterpreter()
    interpreter.interpretPath("RecipeTest")
def DefineUserFunctionsTest():
    interpreter = setupInterpreter()
    interpreter.interpretPath("DefineUserFunctionsTest")
def ConstantsTest():
    interpreter = setupInterpreter()
    interpreter.interpretPath("ConstantsTest")
def LoopBreakAndWaitTest():
    interpreter = setupInterpreter()
    interpreter.interpretPath("LoopBreakAndWaitTest")
#Actual impelmenting stuff, run with caution
# ManifestTest()
# NamespaceTest()
# RecipeTest()
# LoadAndTickTest()
# DefineUserFunctionsTest()
# ConstantsTest()
# LoopBreakAndWaitTest()

