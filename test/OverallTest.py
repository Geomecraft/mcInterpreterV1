from model.Interpreter import Interpreter
import os

#change path to mcInterpreterV1
# print(os.getcwd())
parentPath = os.path.dirname(os.getcwd())
os.chdir(parentPath)
# print(os.getcwd())

#helpers
def assertException(testPath, exceptionMessage):
    try:
        Interpreter.interpret(testPath, True, False)
        assert (False)
    except Exception as e:
        assert (str(e) == exceptionMessage)



#actual tests
def ManifestTest():
    interpreter = Interpreter()
    interpreter.options.datapackOutputPath = "/output"
    interpreter.interpret("test/ManifestTest")
def RecipeTest():
    interpreter = Interpreter()
    interpreter.options.datapackOutputPath = "/output"
    interpreter.interpret("test/RecipeTest")

#Actual impelmenting stuff, run with caution
# ManifestTest()
RecipeTest()

