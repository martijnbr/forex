import os
import datetime as dt

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def time_to_datetime(time):
    return dt.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
        
class Selector:
    def __init__(self, arr):
        if isinstance(arr, dict):
            arr = list(arr.values())
        self.list = arr
    def __add__(self, other):
        ownname = self.__class__
        othername = other.__class__
        if not ownname == othername:
            raise TypeError("Unsuported addition: {0} and {1}".format(ownname, othername))
        return self.__class__(self.list + other.list)
        
class Iterator:
    def __init__(self, list):
        self.list = list
        self.index = -1
        
    def next(self):
        self.index += 1
        return self.list[self.index]

    def hasNext(self):
        return len(self.list[self.index+1:]) > 0
    
    def length(self):
        return len(self.list)
    
    def __add__(self, other):
        ownname = self.__class__
        othername = other.__class__
        if not ownname == othername:
            raise TypeError("Unsuported addition: {0} and {1}".format(ownname, othername))
        return Iterator(self.list + other.list)
    
