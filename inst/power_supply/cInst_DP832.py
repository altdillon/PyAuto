from cInst_power_supply import cInst_power_supply

def cInst_DP832(inst, inst_id, connection_mode, address):
    return [cInst_DP832_1(inst, inst_id, connection_mode, address),
            cInst_DP832_2(inst, inst_id, connection_mode, address),
            cInst_DP832_3(inst, inst_id, connection_mode, address)]

class cInst_DP832_1(cInst_power_supply):
    '''
    TBD
    '''
    def set_channel(self):
        '''
        Sets the channel since this is a multi-channel supply
        '''
        self.comm(":INST:NSEL 1")

class cInst_DP832_2(cInst_power_supply):
    '''
    TBD
    '''
    def set_channel(self):
        '''
        Sets the channel since this is a multi-channel supply
        '''
        self.comm(":INST:NSEL 2")

class cInst_DP832_3(cInst_power_supply):
    '''
    TBD
    '''
    def set_channel(self):
        '''
        Sets the channel since this is a multi-channel supply
        '''
        self.comm(':INST:NSEL 3')
        