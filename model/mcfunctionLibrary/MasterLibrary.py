from model.mcfunctionLibrary import BuiltInFunction
from model.mcfunctionLibrary import Cinematics

GlobalBuiltInFunctionsDict = {}
LocalBuiltInFunctionsDict = {}

GlobalBuiltInFunctionsDict.update(BuiltInFunction.GlobalBuiltInFunctionsDict)
GlobalBuiltInFunctionsDict.update(Cinematics.GlobalBuiltInFunctionsDict)
LocalBuiltInFunctionsDict.update(BuiltInFunction.LocalBuiltInFunctionsDict)
LocalBuiltInFunctionsDict.update(Cinematics.LocalBuiltInFunctionsDict)

if __name__ == "__main__":
    print(GlobalBuiltInFunctionsDict)
    print(LocalBuiltInFunctionsDict)