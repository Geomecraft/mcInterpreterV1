class try1:
    def __init__(self):
        self.one = "asdf"
        self.two = self.one


lol = try1()
lol.one = ("qwer")
print(lol.two)