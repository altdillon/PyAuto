from cInst_power_supply import cInst_power_supply
from types import FunctionType

def cInst_E3631A(inst, inst_id, connection_mode, address):
    return [cInst_E3631A_1(inst, inst_id, connection_mode, address),
            cInst_E3631A_2(inst, inst_id, connection_mode, address),
            cInst_E3631A_3(inst, inst_id, connection_mode, address)]

class cInst_E3631A_1(cInst_power_supply, metaclass = Meta):
    '''
    TBD
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        cInst_power_supply.__init__(self, inst, inst_id, connection_mode, address)
        self.channel = 1

    pass

class cInst_E3631A_2(cInst_power_supply, metaclass = Meta):
    '''
    TBD
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        cInst_power_supply.__init__(self, inst, inst_id, connection_mode, address)
        self.channel = 2

    pass

class cInst_E3631A_3(cInst_power_supply, metaclass = Meta):
    '''
    TBD
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        cInst_power_supply.__init__(self, inst, inst_id, connection_mode, address)
        self.channel = 3

    pass

def wrapper(channel):
    def inner(method):
        def wrapped(*args, **kwargs):
            self.set_channel(self.channel)
            method(*args, **kwargs)
        return wrapped
    return inner

class Meta(type):
    def __new__(cls, name, bases, dct):
        newdct = {}
        for attributeName, attribute in dct.items():
            if isinstance(attribute, FunctionType):
                attribute = wrapper(attribute)
            newdct[attributeName] = attribute
        return super().__new__(cls, name, bases, newdct)