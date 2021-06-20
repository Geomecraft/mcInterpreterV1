from model import Interpreter
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

# def printDebug(debugInfo):
#     for i in debugInfo[0]:
#         print(i)
#     print(debugInfo[1])



#function closing syntax
assert Interpreter.FUNCTION_CLOS_SYNTAX.fullmatch("}")
assert Interpreter.FUNCTION_CLOS_SYNTAX.fullmatch("} ")
assert not Interpreter.FUNCTION_CLOS_SYNTAX.fullmatch("}}")
assert not Interpreter.FUNCTION_CLOS_SYNTAX.fullmatch("{")
assert not Interpreter.FUNCTION_CLOS_SYNTAX.fullmatch("{}")



#variable definition/assignment syntax
assert Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("a = 3")
assert Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("ab = a")
assert Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("ab = \\a")
assert Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("ab = I am lol")
assert Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("Lol = \"32\"")
assert Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("Lsdgrol = return()")
assert Interpreter.VARIABLE_ASI_SYNTAX.fullmatch(" Lsdgrol = return()")
assert Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("    Lsdgrol = return()")
assert Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("Lsdgrol=return()")
assert not Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("? = 3")
assert not Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("end() = 3")
assert not Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("end() = end()")
assert not Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("= 3")
assert not Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("3")
assert not Interpreter.VARIABLE_ASI_SYNTAX.fullmatch("")



#variable assining literal, forced literal, and value of other variable test
# print(Interpret.interpret("test/assigningVarTest1", True, True))



#Read function definition test
# print(Interpret.interpret("test/readNewFunctionDefinitionTest1", True, True))
# assertException("test/readNewFunctionDefinitionTest2","At line 1, AbstractionError: Non-abstract functions cannot have arguments")



#Read builtin function usage test
# assertException("test/readBuiltInFunctionUsageTest1", "At line 2 for function Manifest, expected 3 arguments, got 1 arguments instead")
# assertException("test/readBuiltInFunctionUsageTest2", "At line 1 for function manefast, no such function found in built-in functions")
# assertException("test/readBuiltInFunctionUsageTest3", "At line 5 for function recipe.shaped, no current namespace is set")
# assertException("test/readBuiltInFunctionUsageTest4", "At line 6 for function recipe.shaped, expected 7, or 12 arguments, got 6 arguments instead")
# assertException("test/readBuiltInFunctionUsageTest5", "At line 1 for function Manifest, expected int type, got string instead")
# assertException("test/readBuiltInFunctionUsageTest6", "At line 4 for function recipe.shapeless, expected 4-12 arguments, got 3 arguments instead")
# assertException("test/readBuiltInFunctionUsageTest7", "At line 5 for function recipe.shapeless, expected 4-12 arguments, got 13 arguments instead")


#Actual impelmenting stuff, run with caution
# print(Interpret.interpret("test/ManifestImplementTest", True, False))
print(Interpreter.interpret("test/RecipeImplementTest", True, False))