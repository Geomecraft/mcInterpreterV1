from model.Interpreter import Interpreter

def setContentTest():
    interpreter = Interpreter()
    interpreter.setContent("setContentTestFile")
    assert (interpreter.content == ['placeHolder', '    some content', 'some other content', '', 'new line before', 'new line after', '', 'lol'])
setContentTest()

def setCurrentLineTest():
    interpreter = Interpreter()
    interpreter.setContent("setCurrentLineTestFile")
    interpreter.setCurrentLine()
    assert(interpreter.currentLine == "some content")
setCurrentLineTest()

def isFunctionDefinitionTest():
    interpreter = Interpreter()
    #true tests
    interpreter.currentLine = "def Manifest(){"
    assert interpreter.isFunctionDefinition()
    interpreter.currentLine = "def abstract enf(e, ph){"
    assert interpreter.isFunctionDefinition()
    interpreter.currentLine = "def Biom?(){"
    assert interpreter.isFunctionDefinition()
    interpreter.currentLine = "def  Manifest(parameter1, parameter 2){"
    assert interpreter.isFunctionDefinition()
    interpreter.currentLine = "def     abstract     Manifest()  {"
    assert interpreter.isFunctionDefinition()
    #false tests
    interpreter.currentLine = "def (){"
    assert not interpreter.isFunctionDefinition()
    interpreter.currentLine = "def try{"
    assert not interpreter.isFunctionDefinition()
    interpreter.currentLine = "def abstract"
    assert not interpreter.isFunctionDefinition()
    interpreter.currentLine = "random()"
    assert not interpreter.isFunctionDefinition()
    interpreter.currentLine = "abstract random()"
    assert not interpreter.isFunctionDefinition()
isFunctionDefinitionTest()

def isFunctionUsageTest():
    interpreter = Interpreter()
    interpreter.currentLine = "Manifest()"
    assert interpreter.isFunctionUsage()
    interpreter.currentLine = "enf(34, ph)"
    assert interpreter.isFunctionUsage()
    interpreter.currentLine = "Biom?()"
    assert interpreter.isFunctionUsage()
    interpreter.currentLine = "Manifest!(argument1,argument2)"
    assert interpreter.isFunctionUsage()
    interpreter.currentLine = "try(7843r0e9itwruy,)"
    assert interpreter.isFunctionUsage()
    #false tests
    interpreter.currentLine = "def Manifest(){"
    assert not interpreter.isFunctionUsage()
    interpreter.currentLine = "enf"
    assert not interpreter.isFunctionUsage()
    interpreter.currentLine = "enf{"
    assert not interpreter.isFunctionUsage()
    interpreter.currentLine = "random ()"
    assert not interpreter.isFunctionUsage()
    interpreter.currentLine = "()"
    assert not interpreter.isFunctionUsage()
isFunctionUsageTest()

def interpretAsFunctionDefinitionTest():
    def readAbstractFunctionOnlyCommands():
        interpreter = Interpreter()
        interpreter.interpret("interpretAsFunctionDefinitionTestFile_readAbstractFunctionOnlyCommands")
        fn = interpreter.memory.memory["smiteWithinDistance"]
        assert (fn.name == "smiteWithinDistance")
        assert (fn.parameters == ['centerEntity', 'smiteEntityType', 'distance'])
        assert (fn.definition == ['execute at <centerEntity> run execute at @e[type=<smiteEntityType>,distance=..<distance>] run summon lightning_bolt ~ ~ ~', 'msg <centerEntity> somebody tried to go close to you within distance <distance>, and got snipped'])
        assert (fn.abstraction == True)
    readAbstractFunctionOnlyCommands()
interpretAsFunctionDefinitionTest()

    