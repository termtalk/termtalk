'''
This module provides a shared storage class that can be used to store data
'''

class Storage:
    '''
    A class to provide shared storage
    '''

    _instance = None
    _data = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Storage, cls).__new__(cls)
            cls._instance._data = {}  # Initialize the shared data dictionary
        return cls._instance

    def set(self, key, value):
        '''
        Set a value in the storage
        '''
        self._data[key] = value

    def get(self, key, default=None):
        '''
        Get a value from the storage
        '''
        return self._data.get(key, default)

    def isset(self, key):
        '''
        Check if a key is set in the storage
        '''
        return key in self._data

    def remove(self, key):
        '''
        Remove a key from the storage
        '''
        if key in self._data:
            del self._data[key]

    def clear(self):
        '''
        Clear the storage
        '''
        self._data.clear()
