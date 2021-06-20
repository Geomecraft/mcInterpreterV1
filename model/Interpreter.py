#Line based intepretation
"testInput.txt"
import re
from model import BuiltInFn
from model.DebugLog import DebugElementInfo, DebugElementMemory, DebugLog
from model.Exceptions import AbstractionError, IncorrectArguments, SyntaxError, NullError
from model.Function import Function
from model.Options import Options


class Interpreter:
    def __init__(self, content = None, memory=None, currentLineNumber=1, currentLineString = "", options=None, debugLog=None):
        if memory is None:
            memory = {}
        if options is None:
            options = Options()
        if debugLog is None:
            debugLog = DebugLog()
        self.content = content #type list of string
        self.memory = memory #type Memory
        self.currentLineNumber = currentLineNumber #type int
        self.currentLine = currentLineString #type string
        self.options = options #type Options
        self.debugLog = debugLog #type DebugLog

    #EFFECTS: read in all of a certain file, and then store the information as a list with each element representing a line. list Index is lined up with line number
    #MODIFIES: this.content
    def setContent(self, filePath):
        f = open(filePath, "r")
        self.content = ["placeHolder"] #so list index line up with line number
        self.content += f.read().split("\n")
        f.close()

    #EFFECTS: extract the line in string corresponding to the current line number to be processed. Begining and end spaces are removed since indent does not matter in this language.
    #MODIFIES: this.content
    def setCurrentLine(self):
        self.currentLine = self.content[self.currentLineNumber].strip()


    #EFFECTS: see if this line of code is suppose to do X (for all isX function below)
    def isComment(self):
        pass

    def isVariableAssignment(self):
        pass

    def isFunctionDefinition(self):
        FUNCTION_DEFINITION_SYNTAX = re.compile(r"def\s+(abstract\s+)?(\S)+\(.*")
        return FUNCTION_DEFINITION_SYNTAX.fullmatch(self.currentLine)

    def isFunctionUsage(self):
        FUNCTION_USAGE_SYNTAX = re.compile(r"(\S)+\(.*")
        return FUNCTION_USAGE_SYNTAX.fullmatch(self.currentLine)


    #EFFECTS: do nothing because it is a comment
    def interpretAsComment(self):
        pass

    #EFFECTS: write in memory that the name of the varible can access its value (the varialbe object)
    def interpretAsVariableAssignment(self):
        pass

    def interpretAsFunctionDefinition(self):
        pass

    #EFFECTS: if it is a build in function, execute its function. If it is a user defined function, return its minecraft command line body equivalence
    def interpretAsFunctionUsage(self):
        pass



    def interpret(self, filePath):
        self.setContent(filePath)
        maximumLineNumber = len(self.content)

        while (self.currentLineNumber <= maximumLineNumber):
            self.setCurrentLine()
            if self.isComment():
                self.interpretAsComment()
            elif self.isVariableAssignment():
                self.interpretAsVariableAssignment()
            elif self.isFunctionDefinition():
                self.interpretAsFunctionDefinition()
            elif self.isFunctionUsage():
                self.interpretAsFunctionUsage()




FUNCTION_DEF_SYNTAX = re.compile(r"def\s+(abstract\s+)?(\S)+\(")
FUNCTION_CLOS_SYNTAX = re.compile(r"}\s*")
VARIABLE_ASI_SYNTAX = re.compile(r"\s*\w+\s?=\s?(\S|\s)+")
FUNCTION_USE_SYNATX = re.compile(r"(\w|\?)+\((\S|\s)*\)")
FUNCTION_RELATED_SYNATX = re.compile(r"(def\s+)?(abstract\s+)?(\w|\?|\.)+\((\S|\s)*")

BUILT_IN_FN = BuiltInFn.BuiltInFunctionsDict

#EFFECTS: read in a regular function's parameter, and convert them into a list of each element of the parameter, when the string is missing the first opening bracket:
#SIGNATURE: String -> listof(String)
#EXAMPLE: 2 , You Are Good) -> ["2","You Are Good"]
def halfParameterSplicing(s):
    temp = s.split(")")[0].split(",")
    for i in range(0,len(temp)):
        temp[i] = temp[i].strip()
    return temp

def interpret(filePath, debug=False, noImplement=False):
    f = open(filePath, "r")
    input = f.read().split("\n")
    output = ""
    f.close()


    #System things
    infoLog = []
    debugLog = DebugLog([],[])
    memory = {}
    i = 0



    # EFFECTS: read in the name, parameters and body of a function definition
    # SIGNATURE (string -> [string, listof(string), listof(string), boolean])
    def readFnDef(s):
        nonlocal i
        nonlocal input

        #read in name and parameters, and is it abstract
        if (s[0:8] == "abstract"):
            isAbstract = True
            s = s[8:].strip()
        else:
            isAbstract = False
        sList = s.split("(")
        name = sList[0]
        lop = halfParameterSplicing(sList[1])
        loc = []

        if ((not isAbstract) and lop != ['']):  # throw exception if non-abstract function has arguments
            raise AbstractionError("At line " + str(i + 1) + ", AbstractionError: Non-abstract functions cannot have arguments")

        i += 1
        s = input[i]
        #change line number depending on how much line this function takes
        while(not FUNCTION_CLOS_SYNTAX.fullmatch(s)):
            #read in function body
            loc.append(s.strip())
            i += 1
            s = input[i]

        result = [name, lop, loc, isAbstract] #name, list of parameters, list of commands
        if debug:
            infoLog.append(result)
        return result

    # EFFECTS: use the read in information and write relevant information into program memory
    # SIGNATURE ([string, listof(string), listof(string), boolean] -> string)
    def memorizeFnDef(loi):
        nonlocal memory

        if (loi[3]): #Now the name of the funciton maps to the [lop, loc, True], it is an abstract function
            memory[loi[0]] = loi[1:]
        else:   #A non-abstract function needs no memorize and is implemented later in data pack
            pass

    # EFFECTS: use the read in information to cause effects on actual files and content of the data pack
    # SIGNATURE ([string, listof(string), listof(string), boolean] -> void)
    def implementFnDef(loi):
        if noImplement:
            pass
        else: #do stuff
            pass

    # EFFECTS: read in the name, parameters and body of a function in usage
    # SIGNATURE (string -> [string, listof(string)])
    def readFnUse(s):

        # read in name and parameters,
        sList = s.split("(")
        name = sList[0]
        lop = halfParameterSplicing(sList[1])

        result = [name, lop]  # name, list of parameters
        if debug:
            infoLog.append(result)
        return result

    # EFFECTS: use the read in information and write relevant information into program memory
    # SIGNATURE ([string, listof(string)] -> string)
    def memorizeFnUse(loi):
        pass

    # EFFECTS: use the read in information to cause effects on actual files and content of the data pack
    # SIGNATURE ([string, listof(string)] -> void)
    def implementFnUse(loi):
        if noImplement:
            pass
        else: #do stuff
            nonlocal memory

            name = loi[0]
            arguments = loi[1]
            if name in BUILT_IN_FN.keys(): #if it is a built in function

                try:
                    debugInfo = BUILT_IN_FN[name](arguments)
                except IncorrectArguments as e:
                    raise IncorrectArguments("At line " + str(i + 1) + " for function " + name + ", " + str(e))

                if debug:
                    infoLog.append(debugInfo)

            else:
                #TODO
                FnInfo = memory[name]





    # EFFECTS: read in the assignment or creation of a variable
    # SIGNATURE (string -> [string, string])
    def readVar(s):
        lst = s.split("=")
        result = [i + 1,lst[0].strip(),lst[1].strip()]
        if debug:
            debugLog.loi.append(DebugElementInfo(result,i))
        return result
        #return format: [varName, varValue]

    # EFFECTS: use the read in information and write relevant information into program memory
    # SIGNATURE ([string, String] -> void)
    def memorizeVar(loi):
        varName = loi[0]
        varValue = loi[1]
        if FUNCTION_USE_SYNATX.fullmatch(varValue):  #the value is a function, assign the variable by the return value of the function
            pass
        elif varValue in memory.keys():  #the value is a variable, assign the variable by pass in value
            memory.update({varName:memory[varValue]})
        else:  #the value is literal (or forced literal), straight up assigning
            if varValue[0] == "\\":
                memory.update({varName:varValue[1:]})
            else:
                memory.update({varName:varValue})

    # EFFECTS: use the read in information to cause effects on actual files and content of the dtat pack
    # SIGNATURE ([string, String] -> void)
    def implementVar(loi):
        #pass because assigning variable do nothing to the datapack itself
        pass


    def readFunctionRelated(s):
        nonlocal i
        fnInfo = Function.asEmpty()
        originali = i

        #get basic info, and basically deconstruct the string
        if re.compile(r"def\s+(\S|\s)*").fullmatch(s):
            fnInfo.definition = True
            s = s[3:].strip()
            if re.compile(r"(abstract\s+)(\S|\s)*").fullmatch(s):
                fnInfo.abstraction = True
                s = s[8:].strip()
            else:
                fnInfo.abstraction = False
        else:
            fnInfo.definition = False

        #read in name and chop it off
        index = s.find("(")
        fnInfo.name = s[:s.find("(")]
        s = s[index+1:]

        #read in arguments, and chop it off
        def readInArguments():
            nonlocal s
            nonlocal i
            escape = False
            loa = []
            thisArgument = ""
            while True:
                for ii in range(0,len(s)):
                    if escape:  # escapes
                        thisArgument += s[ii]
                        escape = False
                    elif s[ii] == "\\": #escape character? If yes, then next character will be escaped
                        escape = True
                    elif s[ii] == ",":  # indicates next argument
                        loa.append(thisArgument)
                        thisArgument = ""
                    elif s[ii] == ")": #arguments phase ends
                        loa.append(thisArgument)
                        loa.append(ii)
                        return loa
                    else: #not a special character
                        thisArgument += s[ii]
                i += 1
                s = input[i]
        loa = readInArguments()
        index = loa[-1]
        loa.pop()
        for ii in range(0,len(loa)):
            loa[ii] = loa[ii].strip()
        if fnInfo.definition:
            fnInfo.parameters = loa
        else:
            fnInfo.arguments = loa
        s = s[index + 1:]

        if (fnInfo.definition and (not fnInfo.abstraction) and fnInfo.parameters != ['']):
            raise AbstractionError(
                "At line " + str(i + 1) + ", AbstractionError: Non-abstract functions cannot have arguments")

        #read in possible definition
        def readInFnBody():
            nonlocal s
            nonlocal i
            loc = []

            #use interpret???

            while True:
                if VARIABLE_ASI_SYNTAX.fullmatch(s):  # variable assignment/decleartion
                    pass
                elif FUNCTION_RELATED_SYNATX.fullmatch(s):  # possibly multiple line syntax, reoganize them into one command per line
                    pass
                elif re.compile(r"\s*}\s*").fullmatch(s): #function body ends, return
                    return loc
                else:
                    loc.append(s.strip())   #append this line of command onto loc
                i += 1
                s = input[i]


        if fnInfo.definition:
            if re.compile(r"\s*{\s*").fullmatch(s): #{ this line
                i += 1
                s = input[i]
                pass
            elif re.compile(r"\s*{\s*").fullmatch(s + input[i+1]): #{ next line
                i += 2
                s = input[i]
                pass
            else:
                raise SyntaxError("At line " + str(i + 1) + ", expecting function body, encountered none")
            fnInfo.body = readInFnBody()

        if debug:
            debugLog.loi.append(DebugElementInfo(fnInfo,originali))
        return fnInfo

    def memorizeFunctionRelated(loi):
        pass

    def implementFunctionRelated(fnInfo):
        if noImplement:
            pass
        else: #do stuff
            nonlocal memory
            debugInfo = ""

            if fnInfo.definition:
                # TODO
                pass
            else: #is not definition
                if fnInfo.name in BUILT_IN_FN.keys(): #if it is a built in function
                    try:
                        debugInfo = BUILT_IN_FN[fnInfo.name](fnInfo.arguments,memory)
                    except Exception as e:
                        raise Exception("At line " + str(i + 1) + " for function " + fnInfo.name + ", " + str(e))
                else:
                    raise NullError("At line " + str(i + 1) + " for function " + fnInfo.name + ", no such function found in built-in functions")

            if debug:
                debugLog.loi.append(DebugElementInfo(debugInfo,i))

    #Actual loop starts
    while(i < len(input)):
        currentInput = input[i].strip()
        if VARIABLE_ASI_SYNTAX.fullmatch(currentInput): #variable assignment/decleartion
            info = readVar(currentInput)
            memorizeVar(info)
            implementVar(info)
        elif FUNCTION_RELATED_SYNATX.fullmatch(currentInput): #possibly multiple line syntax, reoganize them into one command per line
            info = readFunctionRelated(currentInput)
            memorizeFunctionRelated(info)
            implementFunctionRelated(info)
        else:
            pass
        debugLog.lom.append(DebugElementMemory(memory,i))
        i += 1


    if debug:
        return debugLog
