
from model.Exceptions import NullError, ScopeError
from model.Memory import Memory
from model.Parser import parseFunctionUsage
from model.Syntax import isComment, isLocalBuiltInFunctionUsage, isFunctionUsage, isGlobalBuiltInFunctionUsage
import model

LocalBuiltInFunctionsDict = model.BuiltInFunction.LocalBuiltInFunctionsDict

class LocalInterpreter:

    def __init__(self, parentInterpreter=None, incompletefn=None, content=None, memory=None):
        if parentInterpreter is None:
            raise NullError("No parent interpreter when calling local interpreter")
        if content is None:
            content = []
        if memory is None:
            memory = Memory()
        self.parentInterpreter = parentInterpreter
        self.currentLineNumber = 1
        self.incompletefn = incompletefn
        self.setContent(content)  # type list of string, first element is always "placeHolder" so list index line up with line number
        self.memory = memory  # type Memory

    def setContent(self, los):
        self.content = ["placeholder"] + los
        self.maximumLineNumber = len(los)

    def getCurrentLine(self):
        return self.content[self.currentLineNumber].strip()

    def exceptionLineMsg(self):
        #TODO
        # this line message only works for literal lines, does not work if local interpreter is used implicitly or called again
        # how do we fix this?
        return "At line " + str(self.currentLineNumber + self.parentInterpreter.currentLineNumber) + ", "

    def interpretAsComment(self):
        self.incompletefn.definition.append(self.getCurrentLine())

    def interpretAsFunctionUsage(self):
        pass

    def interpretAsLocalBuiltInFunctionUsage(self, fnName, fnlop):
        LocalBuiltInFunctionsDict[fnName](self.parentInterpreter, self.incompletefn, *fnlop)

    def interpret(self, supressLineNumberUpdate = False):
        while (self.currentLineNumber <= self.maximumLineNumber):
            if isComment(self.getCurrentLine()):
                self.interpretAsComment()
            elif isFunctionUsage(self.getCurrentLine()):
                fnName = parseFunctionUsage(self.getCurrentLine())[0]
                fnlop = parseFunctionUsage(self.getCurrentLine())[1]

                if isLocalBuiltInFunctionUsage(self.getCurrentLine()):
                    self.interpretAsLocalBuiltInFunctionUsage(fnName, fnlop)
                elif isGlobalBuiltInFunctionUsage(self.getCurrentLine()):
                    raise ScopeError(
                        self.exceptionLineMsg() + "Cannot call global built in function from within a mcfunction")
                else:  # abstract function
                    expandedAbstractFn = self.parentInterpreter.memory.function[fnName].useAbstractFn(fnlop)
                    local2Interpreter = LocalInterpreter(self.parentInterpreter, self.incompletefn, expandedAbstractFn, self.memory)
                    local2Interpreter.interpret(supressLineNumberUpdate=True)
            else:
                self.incompletefn.definition.append(self.getCurrentLine())
            self.currentLineNumber += 1

        if not supressLineNumberUpdate:
            self.parentInterpreter.currentLineNumber = self.parentInterpreter.currentLineNumber + self.currentLineNumber





