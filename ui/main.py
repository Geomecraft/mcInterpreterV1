from model.Interpreter import Interpreter
from os import listdir, getcwd

#clean output

#produce new data pack
filelist = listdir(getcwd() + "/input")
for i in range(0,len(filelist)):
    interpreter = Interpreter()
    interpreter.options.datapackOutputPath = "/output"
    interpreter.interpret("input/" + filelist[i])
