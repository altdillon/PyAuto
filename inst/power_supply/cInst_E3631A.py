from cInst_power_supply import cInst_power_supply
from types import FunctionType

def cInst_E3631A(inst, inst_id, connection_mode, address):
    return [cInst_E3631A_1(inst, inst_id, connection_mode, address),
            cInst_E3631A_2(inst, inst_id, connection_mode, address),
            cInst_E3631A_3(inst, inst_id, connection_mode, address)]

class cInst_E3631A_1(cInst_power_supply):
    '''
    TBD
    '''
    def set_channel(self):
        '''
        Sets the channel since this is a multi-channel supply
        '''
        self.comm("INST:SEL P6V")

class cInst_E3631A_2(cInst_power_supply):
    '''
    TBD
    '''
    def set_channel(self):
        '''
        Sets the channel since this is a multi-channel supply
        '''
        self.comm("INST:SEL P25V")

class cInst_E3631A_3(cInst_power_supply):
    '''
    TBD
    '''
    def set_channel(self):
        '''
        Sets the channel since this is a multi-channel supply
        '''
        self.comm('INST:SEL N25V')
