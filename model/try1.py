# class try1:
#     def __init__(self, name, fn, numParameterCheck, typeParameterCheck, otherPreConditionChec):
#         if fn == None:
#             fn = lambda x : x
#         self.name = name    #type string
#         self.fn = fn    #type function literal
#         self.numParameterCheck = numParameterCheck      #type function literal
#         self.typeParameterCheck = typeParameterCheck     #type function literal
#         self.otherPreConditionCheck = otherPreConditionChec     #type function literal
#         def use(interpreter, loa):
#             self.numParameterCheck(loa)
#             self.typeParameterCheck(loa)
#         self.use
# def readFunctionUsageOld(fnstr):
#     fnName = fnstr.split("(", 1)[0]
#     fnlop = fnstr.split("(", 1)[1][:-1].split(",")
#     return fnName, fnlop

# def readFunctionUsage(fnstr):
#     fnName = fnstr.split("(", 1)[0]
#     lopstr = fnstr.split("(",1)[1].rsplit(")",1)[0]
#
#     fnlop = []
#     lastParseIndex = 0
#     scope = 0
#     ignore = False
#     for i in range(0,len(lopstr)-1):
#         if lopstr[i] == "," and not ignore:
#             fnlop.append(lopstr[lastParseIndex:i])
#             lastParseIndex = i + 1
#         elif (lopstr[i] == "\"" and lopstr[i+1] == "<"):
#             scope += 1
#         elif (lopstr[i] == ">" and lopstr[i+1] == "\""):
#             scope -= 1
#
#         if scope > 0:
#             ignore = True
#         elif scope == 0:
#             ignore = False
#         else:
#             pass
#     fnlop.append(lopstr[lastParseIndex:len(lopstr)])
#
#     #remove the most outer layer of "< and "> for each item, and strip them
#     for i in range(0, len(fnlop)):
#         fnlop[i] = fnlop[i].strip()
#         if fnlop[i][0:2] == "\"<" and fnlop[i][-2:] == ">\"":
#             fnlop[i] = fnlop[i][2:-2]
#
#     return fnName, fnlop
#
import re

name = "NORMAL_NBT_1"
value = "{display:{Name:\'{\"text\":\"Very good egg\"}\'},Enchantments:[{id:\"minecraft:sharpness\",lvl:5s}]})"
tx = "display(>NORMAL_NBT<)"
# print(re.sub(r"[(,]>" + name + "<[(,]", "\"<" + value + ">\"", tx))
# print(re.sub(r"[(,]1[),]", "\"<" + "sub" + ">\"", "(1)"))


whole = "item.modifier.setNBT(compass_setup, tag, >NORMAL_NBT_1<)"
matchObject = re.search(r"([(,]\s*>" + name + "<\s*[),])", whole)
new = whole[:matchObject.start()] + whole[matchObject.start():matchObject.end()].replace(">" + name + "<", "\"<" + value + ">\"") + whole[matchObject.end():]
print(new)