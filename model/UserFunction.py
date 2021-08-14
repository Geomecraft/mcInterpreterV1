from model.General import stripEachItem
from model.BuiltInFunction import GlobalBuiltInFunctionsDict, LocalBuiltInFunctionsDict
from model.Syntax import FUNCTION_USAGE_SYNTAX
from model.Parser import parseFunctionUsage


class UserFunction:

    def __init__(self, name = "", parameters=None, definition=None, abstraction = None, namespace = ""):
        # class invariants:
        # - If a function is a definition, body and arguments are None
        # - If a function is not a definition (its a usage), abstraction, parameters and body are None
        if definition is None:
            definition = []
        if parameters is None:
            parameters = []
        self.name = name  # string
        self.parameters = parameters  # list of string that represents each parameter's name
        self.definition = definition  # list of string that each line represents a line of command, that may have a parameter waiting to be substituted. The parameter waiting to be subtituted must be wrapped in "/" at begining and end
        self.abstraction = abstraction  # bool
        self.namespace = namespace

    def __str__(self):
        if self.abstraction:
            rep = "abstract "
        else:
            rep = ""
        rep += self.name + "("
        for x in self.parameters:
            rep += x
            rep += ", "
        rep = rep[:-2] + ")" + "{\n"
        for x in self.definition:
            rep += x + "\n"
        rep += "}"
        return rep


    #REQUIRES: #los must follow the format of normal function definition, where the first element is the definition clause, such as "def abstract try(p1, p2)", note that there is no "{" at the end, cause the string should have already been cleaned. It is followed by list of commands/functions
    @classmethod
    def constructFromInterpretation(cls, interpreter, los):

        definitionClause = los[0]
        definitionClause = definitionClause[3:].strip() #get rid of "def" and the space

        if (definitionClause[0:9] == "abstract "):
            abstraction = True
            definitionClause = definitionClause[8:].strip() #get rid of "abstract" and the space
        else:
            abstraction = False

        name = parseFunctionUsage(definitionClause)[0]
        parameters = parseFunctionUsage(definitionClause)[1]
        if not abstraction:
            name = interpreter.memory.currentNamespace + ":" + name

        definition = []
        thisfn = cls(name, parameters, definition, abstraction)

        localInterpreter = LocalInterpreter(interpreter, thisfn, los[1:], None)
        localInterpreter.interpret()

        # if len(los) > 1:
        #     for i in range(1,len(los)):
        #         if FUNCTION_USAGE_SYNTAX.fullmatch(los[i]) and los[i][0] != "#": #is a function call, and if it is commented out just add that whatever onto body anyways since it wont run
        #             fnName = parseFunctionUsage(los[i])[0]
        #             fnlop = parseFunctionUsage(los[i])[1]
        #             if fnName in GlobalBuiltInFunctionsDict.keys():
        #                 GlobalBuiltInFunctionsDict[fnName](interpreter, *fnlop)
        #             elif fnName in LocalBuiltInFunctionsDict.keys():
        #                 LocalBuiltInFunctionsDict[fnName](interpreter, thisfn, *fnlop)
        #             else:
        #                 thisfn.definition += interpreter.memory.function[fnName].useAbstractFn(fnlop)
        #         else:
        #             thisfn.definition.append(los[i])
        return thisfn

    def useAbstractFn(self, lop):
        if not self.parameters:
            return self.definition
        else:
            substituedBody = []
            for i in range(0,len(self.definition)):
                substituedLine = self.definition[i]
                for ii in range(0,len(lop)):
                    substituedLine = substituedLine.replace("<" + self.parameters[ii] + ">", lop[ii])
                substituedBody.append(substituedLine)
            return substituedBody


    #helper to implement non-abstract functions
    def commandRepresentation(self):
        str = ""
        for x in self.definition:
            str += x
            str += "\n"
        return str





from model.Exceptions import NullError, ScopeError
from model.Memory import Memory
from model.Syntax import isComment, isLocalBuiltInFunctionUsage, isFunctionUsage, isGlobalBuiltInFunctionUsage


class LocalInterpreter:

    def __init__(self, parentInterpreter=None, incompletefn=None, content=None, memory=None, supressLineNumberUpdate = False):
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
        self.supressLineNumberUpdate = supressLineNumberUpdate

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

    def interpret(self):
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
                    local2Interpreter = LocalInterpreter(self.parentInterpreter, self.incompletefn, expandedAbstractFn, self.memory, True)
                    local2Interpreter.interpret()
            else:
                self.incompletefn.definition.append(self.getCurrentLine())
            self.currentLineNumber += 1

        if not self.supressLineNumberUpdate:
            self.parentInterpreter.currentLineNumber = self.parentInterpreter.currentLineNumber + self.currentLineNumber




