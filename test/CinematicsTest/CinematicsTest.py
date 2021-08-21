#before
from model.FileManage import clearDirectory
from model.GlobalInterpreter import GlobalInterpreter
from model.Options import Options

clearDirectory("output")
def setupInterpreter():
    interpreter = GlobalInterpreter()
    interpreter.options = Options.constructFromJsonFile("option.json")
    return interpreter

#actual tests
def FaceTest():
    interpreter = setupInterpreter()
    interpreter.options.mainFilePath = "FaceTest"
    interpreter.interpretPath()
FaceTest()