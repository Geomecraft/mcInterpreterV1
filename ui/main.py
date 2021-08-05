import json

from model.Interpreter import Interpreter
from os import listdir, getcwd
from model.General import clearDirectory

#clean output
clearDirectory("output")

#produce new data pack
with open("input/option.json","r") as infile:
    options = json.loads(infile.read())
    interpreter = Interpreter()
    interpreter.options.datapackOutputPath = options["outputPath"]
    interpreter.options.datapackInputPath = options["inputPath"]
    interpreter.interpret("/" + options["main"])
    print(interpreter.memory.function)
