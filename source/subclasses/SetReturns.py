# A set class that derives from set
# but return False exception is add() or update() fails otherwise True.
class SetReturns(set):
    
    def add(self, e):
        if e in self:
            return False
        else:
            super().add(e)
            return True

    def update(self, e):
        return self.__ior__(e)

    def __ior__(self, e):
        if any(x in self for x in e):
            return False
        else: 
            super().__ior__(e)
            return True
