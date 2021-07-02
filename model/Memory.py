class Memory:
    def __init__(self, memory=None):
        if memory is None:
            memory = {}
        self.memory = memory #type dict
