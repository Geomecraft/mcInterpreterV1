import json
import os

from model.GlobalInterpreter import GlobalInterpreter
from os import listdir, getcwd
from model.FileManage import clearDirectory

#clean output
from model.Options import Options

#produce new data pack
interpreter = GlobalInterpreter()
interpreter.options = Options.constructFromJsonFile("option.json")
interpreter.interpretPath()