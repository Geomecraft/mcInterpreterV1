class Function:

    def __init__(self, name="", parameters=None, definition=None, abstraction = None):
        # class invariants:
        # - If a function is a definition, body and arguments are None
        # - If a function is not a definition (its a usage), abstraction, parameters and body are None
        if definition is None:
            definition = []
        if parameters is None:
            parameters = []
        self.name = name  # string
        self.parameters = parameters  # list of string
        self.definition = definition  # list of string
        self.abstraction = abstraction  # bool

    def __str__(self):
        return str({"name": self.name, "parameters": self.parameters, "definition": self.definition,
                    "abstraction": self.abstraction})
