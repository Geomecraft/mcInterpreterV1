from model.Interpreter import Interpreter

with open("fileName") as infile:
    fileName = infile.read().split("\"")[1]

interpreter = Interpreter()
interpreter.interpret(fileName)