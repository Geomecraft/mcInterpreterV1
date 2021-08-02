from model.General import stripEachItem, parseFunctionUsage
from model.BuiltInFunction import GlobalBuiltInFunctionsDict, LocalBuiltInFunctionsDict
from model.Syntax import FUNCTION_USAGE_SYNTAX


class UserFunction:

    def __init__(self, name="", parameters=None, definition=None, abstraction = None):
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

        name = definitionClause.split("(")[0]

        parameters = definitionClause.split("(")[1][:-1].split(",")
        stripEachItem(parameters)

        definition = []
        thisfn = cls(name, parameters, definition, abstraction)

        if len(los) > 1:
            for i in range(1,len(los)):
                if FUNCTION_USAGE_SYNTAX.fullmatch(los[i]) and los[i][0] != "#": #is a function call, and if it is commented out just add that whatever onto body anyways since it wont run
                    fnName = parseFunctionUsage(los[i])[0]
                    fnlop = parseFunctionUsage(los[i])[1]
                    if fnName in GlobalBuiltInFunctionsDict.keys():
                        GlobalBuiltInFunctionsDict[fnName](interpreter, *fnlop)
                    elif fnName in LocalBuiltInFunctionsDict.keys():
                        LocalBuiltInFunctionsDict[fnName](interpreter, thisfn, *fnlop)
                    else:
                        thisfn.definition += interpreter.memory.function[fnName].useAbstractFn(fnlop)
                else:
                    thisfn.definition.append(los[i])

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





