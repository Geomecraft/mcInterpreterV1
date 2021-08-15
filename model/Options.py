import json
import os


class Options:
    def __init__(self,recordDebugLog=True, basePath = "", mainFilePath = "", datapackOutputPath = "", datapackInputPath = ""):
        self.recordDebuglog = recordDebugLog
        self.basePath = basePath
        self.mainFilePath = mainFilePath
        self.datapackOutputPath = datapackOutputPath
        self.datapackInputPath = datapackInputPath

    @classmethod
    def constructFromJsonFile(cls, fileName):
        with open(fileName, "r") as infile:
            optDict = json.loads(infile.read())
        return cls(optDict.get("debug?", True), os.getcwd(), optDict.get("main", ""), optDict.get("outputPath", ""), optDict.get("inputPath", ""))