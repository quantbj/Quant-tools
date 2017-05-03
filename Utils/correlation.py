class CKey():
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
        
    def __hash__(self):
        return hash(str(self.e1)) & hash(str(self.e2))
        
    def __eq__(self, other):
        return self.__hash__() == hash(other)