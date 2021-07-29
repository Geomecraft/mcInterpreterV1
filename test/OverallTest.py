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
def setupInterpreter():
    interpreter = Interpreter()
    interpreter.options.datapackOutputPath = "output"
    return interpreter
#actual tests
def ManifestTest():
    interpreter = setupInterpreter()
    interpreter.interpret("ManifestTest")
def RecipeTest():
    interpreter = setupInterpreter()
    interpreter.interpret("RecipeTest")
def DefineNonAbstractFunctionsTest():
    interpreter = setupInterpreter()
    interpreter.interpret("DefineNonAbstractFunctionsTest")

#Actual impelmenting stuff, run with caution
# ManifestTest()
RecipeTest()
# DefineNonAbstractFunctionsTest()

