#Line based intepretation
"testInput.txt"
import os
import re
from model import BuiltInFunction
from model.DebugLog import DebugElementInfo, DebugElementMemory, DebugLog
from model.Exceptions import AbstractionError, IncorrectArguments, SyntaxError, NullError
from model.General import stripEachItem, parseFunctionUsage, assertExistNamespace
from model.Syntax import CONSTANT_DEFINITION_SYNTAX, FUNCTION_USAGE_SYNTAX, FUNCTION_DEFINITION_SYNTAX
from model.UserFunction import UserFunction
from model.Memory import Memory
from model.Options import Options

#CONSTANTS
BUILT_IN_FN = BuiltInFunction.GlobalBuiltInFunctionsDict

class Interpreter:

    def __init__(self, content = None, memory=None, currentLineNumber=1, maximumLineNumber = None, options=None, debugLog=None):
        if memory is None:
            memory = Memory()
        if options is None:
            options = Options()
        if debugLog is None:
            debugLog = DebugLog()
        self.content = content #type list of string
        self.memory = memory #type Memory
        self.currentLineNumber = currentLineNumber #type int
        self.maximumLineNumber = maximumLineNumber #type int
        self.options = options #type Options
        self.debugLog = debugLog #type DebugLog

    #EFFECTS: read in all of a certain file, and then store the information as a list with each element representing a line. list Index is lined up with line number
    #MODIFIES: self.content
    def setContent(self, filePath):
        f = open(filePath, "r")
        self.content = ["placeHolder"] #so list index line up with line number
        self.content += f.read().split("\n")
        f.close()

    #EFFECTS: extract the line in string corresponding to the current line number to be processed. Begining and end spaces are removed since indent does not matter in this language.
    #MODIFIES: self.getCurrentLine()
    def getCurrentLine(self):
        return self.content[self.currentLineNumber].strip()

    #EFFECTS: line number increases by one and setCurrentLine
    #MODIFIES: self.getCurrentLine() and self.currentLineNumber
    # def gotoNextLine(self):
    #     self.currentLineNumber += 1
    #     self.setCurrentLine()

    def exceptionLineMsg(self):
        return "At line " + str(self.currentLineNumber) + ", "



    #EFFECTS: see if this line of code is suppose to do X (for all isX function below)
    def isComment(self):
        if self.getCurrentLine() != "":
            return self.getCurrentLine()[0] == "#"

    def isConstantDefinition(self):
        return CONSTANT_DEFINITION_SYNTAX.fullmatch(self.getCurrentLine())

    def isFunctionDefinition(self):
        return FUNCTION_DEFINITION_SYNTAX.fullmatch(self.getCurrentLine())

    def isFunctionUsage(self):
        return FUNCTION_USAGE_SYNTAX.fullmatch(self.getCurrentLine())



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
        los = [self.getCurrentLine()[:-1].strip()]
        self.currentLineNumber += 1
        while(self.getCurrentLine() != "}"):
            los.append(self.getCurrentLine())
            self.currentLineNumber += 1
        fn = UserFunction.constructFromInterpretation(self, los)
        self.memory.function[fn.name] = fn
        if not fn.abstraction: #non abstract, need to implement the function
            assertExistNamespace(self.memory)
            with open(self.memory.getCurrentNamespacePath() + "/functions/" + fn.name + ".mcfunction", 'w') as outfile:
                outfile.write(fn.commandRepresentation())

    #EFFECTS: it is a build in function, execute the function.
    def interpretAsFunctionUsage(self):
        fnstr = self.getCurrentLine()
        fnName = parseFunctionUsage(fnstr)[0]
        fnlop = parseFunctionUsage(fnstr)[1]
        if fnName not in BUILT_IN_FN.keys():
            raise NullError(self.exceptionLineMsg() + "function not found in any built-in library")
        else:
            BUILT_IN_FN[fnName](self,*fnlop)



    def interpret(self, filePath):
        self.setContent(self.options.datapackInputPath + filePath)
        originalPath = os.getcwd()
        os.chdir(os.getcwd() + "/" + self.options.datapackOutputPath)
        self.maximumLineNumber = len(self.content) - 1

        while (self.currentLineNumber <= self.maximumLineNumber):
            if self.isComment():
                self.interpretAsComment()
            elif self.isConstantDefinition():
                self.interpretAsConstantDefinition()
            elif self.isFunctionDefinition():
                self.interpretAsFunctionDefinition()
            elif self.isFunctionUsage():
                self.interpretAsFunctionUsage()
            self.currentLineNumber += 1

        #change back to original path
        os.chdir(originalPath)

#TODO
# refactor all syntax related method from interpreter into file Syntax, and they no longer belong to this class.