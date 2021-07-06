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