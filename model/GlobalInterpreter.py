#Line based intepretation
"testInput.txt"
import os
import re
from model.mcfunctionLibrary import BuiltInFunction, MasterLibrary
from model.DebugLog import DebugLog
from model.Exceptions import NullError
from model.General import assertExistNamespace
from model.Syntax import isComment, \
    isConstantDefinition, isFunctionDefinition, isFunctionUsage
from model.Parser import parseFunctionUsage
from model.UserFunction import UserFunction
from model.Memory import Memory
from model.Options import Options

#CONSTANTS

class GlobalInterpreter:

    def __init__(self, content= None, memory=None, currentLineNumber=1, options=None, debugLog=None):
        if content is None:
            content = []
        if memory is None:
            memory = Memory()
        if options is None:
            options = Options()
        if debugLog is None:
            debugLog = DebugLog()
        self.setContent(content) #type list of string, first element is always "placeHolder" so list index line up with line number
        self.memory = memory #type Memory
        self.currentLineNumber = currentLineNumber #type int
        self.options = options #type Options
        self.debugLog = debugLog #type DebugLog
        self.builtInFn = MasterLibrary.GlobalBuiltInFunctionsDict

    def setContent(self,los):
        self.content = ["placeholder"] + los
        self.maximumLineNumber = len(los)

    def setContentFromPath(self):
        if self.options.datapackInputPath != "":
            self.options.datapackInputPath += "/"
        with open(self.options.datapackInputPath + self.options.mainFilePath, "r") as infile:
            self.setContent(infile.read().split("\n"))

    def getCurrentLine(self):
        return self.content[self.currentLineNumber].strip()

    def exceptionLineMsg(self):
        return "At line " + str(self.currentLineNumber) + ", "

    def fetchFromInput(self, filePathRelativeToInput):
        originalPath = os.getcwd()
        os.chdir(self.options.basePath + "/" + self.options.datapackInputPath)
        with open(filePathRelativeToInput + ".json", "r") as infile:
            str = infile.read()
        os.chdir(originalPath)
        return str

    #EFFECTS: do nothing because it is a comment
    def interpretAsComment(self):
        pass

    #EFFECTS: write in memory that the name of the constant, and all constants later are interpreted as this value
    def interpretAsConstantDefinition(self):
        name = self.getCurrentLine().split("=")[0].strip()
        value = self.getCurrentLine().split("=")[1].strip()
        self.memory.constant[name] = value
        for i in range(1, self.maximumLineNumber + 1):
            matchObject = re.search(r"([(,]\s*>" + name + "<\s*[),])", self.content[i])
            if matchObject:
                self.content[i] = self.content[i][:matchObject.start()] + self.content[i][matchObject.start():matchObject.end()].replace(">" + name + "<", "\"<" + value + ">\"") + self.content[i][matchObject.end():]
            else:
                self.content[i] = self.content[i].replace(">" + name + "<", value)

    #EFFECTS: write the newly defined function in memory, and implement it if it is not an abstract function
    def interpretAsFunctionDefinition(self):

        #scrapping the function information into los
        #first line
        los = [self.getCurrentLine()[:-1].strip()]
        originalLineNumber = self.currentLineNumber

        #all the other lines
        self.currentLineNumber += 1
        while(self.getCurrentLine() != "}"):
            los.append(self.getCurrentLine())
            self.currentLineNumber += 1
        self.currentLineNumber = originalLineNumber

        #construct and implement function
        fn = UserFunction.constructFromInterpretation(self, los)
        self.memory.function[fn.name] = fn
        if not fn.abstraction: #non abstract, need to implement the function
            assertExistNamespace(self.memory)
            with open(self.memory.getCurrentNamespacePath() + "/functions/" + fn.name.split(":")[1] + ".mcfunction", 'w') as outfile:
                outfile.write(fn.commandRepresentation())

    #EFFECTS: it is a build in function, execute the function.
    def interpretAsFunctionUsage(self):
        fnstr = self.getCurrentLine()
        fnName = parseFunctionUsage(fnstr)[0]
        fnlop = parseFunctionUsage(fnstr)[1]
        if fnName not in self.builtInFn.keys():
            raise NullError(self.exceptionLineMsg() + "function not found in any built-in library")
        else:
            self.builtInFn[fnName](self,*fnlop)

    def interpret(self):
        while (self.currentLineNumber <= self.maximumLineNumber):
            if isComment(self.getCurrentLine()):
                self.interpretAsComment()
            elif isFunctionDefinition(self.getCurrentLine()):
                self.interpretAsFunctionDefinition()
            elif isFunctionUsage(self.getCurrentLine()):
                self.interpretAsFunctionUsage()
            elif isConstantDefinition(self.getCurrentLine()):
                self.interpretAsConstantDefinition()
            self.currentLineNumber += 1
            print(self.currentLineNumber)

    def interpretPath(self):
        self.setContentFromPath()
        os.chdir(self.options.basePath + "/" + self.options.datapackOutputPath)

        self.interpret()

        #change back to original path
        os.chdir(self.options.basePath)

#TODO
# refactor all syntax related method from interpreter into file Syntax, and they no longer belong to this class.