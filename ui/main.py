import json

from model.GlobalInterpreter import GlobalInterpreter
from os import listdir, getcwd
from model.General import clearDirectory

#clean output
from model.Options import Options

clearDirectory("output")

#produce new data pack
interpreter = GlobalInterpreter()
interpreter.options = Options.constructFromJsonFile("option.json")
interpreter.interpretPath()