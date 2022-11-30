# A set class that derives from set
# but raises an exception is add() or update() fails.
class SetReturns(set):
    
    # Raise an exception if the element trying to be added already exists.
    def add(self, e):
        if e in self:
            return False
        else:
            super().add(e)
            return True

    # Raises an exception if the element trying to be updated already exists.
    def update(self, e):
        return self.__ior__(e)

    # Raises an exception if the element trying to be updated in place already exists.
    def __ior__(self, e):
        if any(x in self for x in e):
            return False
        else: 
            super().__ior__(e)
            return True
