'''
Created on Mar 17, 2014

@author: vagrant
'''
class Configuration():
    def __init__(self, configurable = None, display_name = None, data_type = None, value = None,
                 function = None, combo = None, bounds = None):
        self.configurable = configurable
        self.display_name = display_name
        self.data_type = data_type
        self.value = value
        self.function = function
        self.combo = combo
        self.bounds = bounds
        