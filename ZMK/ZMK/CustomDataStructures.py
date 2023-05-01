"""
Purpose of this file is to create custom data structures which are used for the ZMK package
"""


class Array:
    """
    Class is used to represent an array that can dynamically grow, if the array is accessed with an index that is
    out of range then it will create a series of None types up until that index.
    methods are implemented based on the methods of the python list class found in the builtins module, well at least
    the methods I'll be using.
    """

    def __init__(self, *args):
        """__init__"""
        # method allows for the array to be initialized with a list if the first parameter is a list
        if len(args) and isinstance(args[0], list):
            self.__array = args[0]
            self.__length = len(args[0])
            return

        self.__array = []
        """array which will store the values of the array"""
        self.__length = 0
        """length attribute is used to keep track of the length of the array so that the len() method does not have to
        used as often, I would like to bet this is redundant and that python does this but I'm not sure, you
        know what I'll test that out right now. The len method seems to have a time complexity of O(1) which is what I
        suspected, so this attribute is redundant, but hey at least I thought of it, right?"""

    def append(self, item):
        """append"""
        self.__array.append(item)
        self.__length += 1

    def clear(self):
        """clear"""
        self.__array.clear()
        self.__length = 0

    def copy(self):
        """copy"""
        return Array(self.__array.copy())

    def insert(self, index: int, item):
        """insert"""
        if not isinstance(index, int):
            raise TypeError(f"parameter 'index' of type {type(index)} is not an int")

        while self.__length <= index:
            self.__array.append(None)
            self.__length += 1

        self.__array[index] = item

    def pop(self, index: int = -1):
        """pop"""
        if not isinstance(index, int):
            raise TypeError(f"parameter 'index' of type {type(index)} is not an int")
        self.__length -= 1
        return self.__array.pop(index)

    def __setitem__(self, key, value):
        """__setitem__"""
        self.insert(key, value)

    def __delitem__(self, key):
        """__delitem__"""
        del self.__array[key]
        self.__length = len(self.__array)

    def __getitem__(self, key):
        """__getitem__"""
        return self.__array[key]

    def __iter__(self):
        """__iter__"""
        return self.__array.__iter__()

    def __len__(self):
        """__len__"""
        return self.__length

    def __str__(self):
        """__str__"""
        return self.__array.__str__()

    def __list__(self):
        """__list__"""
        return self.__array.copy()
