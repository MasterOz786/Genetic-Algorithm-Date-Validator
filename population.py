
from random import randint
import numpy

class Population:
    def __init__(self, size):
        self.__dates = [] # list of tuples of the form (day, month, year)

        # populate
        self.__populate(size)
        return None
    
    # populates __dates with (day, month, year) tuples
    def __populate(self, size):
        __dates = [self.__dates.append((randint(1, 31), randint(1, 12), randint(0000, 9999))) for i in range(size)]

    # getter
    @property
    def dates(self):
        return self.__dates
