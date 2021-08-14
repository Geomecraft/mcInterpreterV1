import json


class Options:
    def __init__(self,recordDebugLog=True, mainFilePath = "", datapackOutputPath = "", datapackInputPath = ""):
        self.recordDebuglog = recordDebugLog
        self.mainFilePath = mainFilePath
        self.datapackOutputPath = datapackOutputPath
        self.datapackInputPath = datapackInputPath

    @classmethod
    def constructFromJsonFile(cls, fileName):
        with open(fileName, "r") as infile:
            optDict = json.loads(infile.read())
        return cls(optDict.get("debug?", True), optDict.get("main", ""), optDict.get("outputPath", ""), optDict.get("inputPath", ""))