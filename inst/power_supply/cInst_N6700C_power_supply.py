from cInst_power_supply import cInst_power_supply

n6700C_modules = [  'N6745B', 'N6752A', 'N6733B', 'N6774A', 
                    'N6735B', 'N6783A', 'N6732B', 'N6736B', 
                    'N6731B', 'N6754A', 'N6753A', 'N6777A', 
                    'N6751A', 'N6761A', 'N6756A', 'N6762A', 
                    'N6776A', 'N6775A', 'N6773A', 'N6746B', 
                    'N6744B', 'N6743B', 'N6741B', 'N6742B', 
                    'N6766A', 'N6764A', 'N6763A', 'N6755A', 
                    'N6734B', 'N6765A']

def cInst_N6700C_power_supply(inst, inst_id, connection_mode, address):
    channels = int(inst.query('SYST:CHAN?'))
    modules = [x for x in inst.query(f'SYST:CHAN:MOD? (@1:{channels})').strip().split(', ') if x in n6700C_modules]
    ret = []
    for i in range(len(modules)):
        ret.append(cInst_N6700C_x(inst, inst_id, connection_mode, address, i+1))
    return ret

class cInst_N6700C_x(cInst_power_supply):
    '''
    TBD
    '''
    def __init__(self, inst, inst_id, connection_mode, address, channel):
        super().__init__(inst, inst_id, connection_mode, address)
        self.channel = channel

    def set_current(self, current):
        '''
        Sets the current limit. Will error if current is set above the supply's capabilities. Set voltage prior to setting current limit
        current : current limit in A
        '''
        self.set_channel()
        #Add error handling (see voltage)
        self.comm(f'CURR {current}, (@{self.channel})')

    def get_current(self):
        '''
        Returns the current limit in A
        '''
        self.set_channel()
        return float(self.comm(f'CURR? (@{self.channel})'))

    def meas_current(self):
        '''
        Returns the measured current from the device in A
        '''
        self.set_channel()
        return float(self.comm(f'MEAS:CURR? (@{self.channel})'))

    def set_voltage(self, voltage):
        '''
        Sets the voltage limit. Will adjust the voltage range (if applicable) to the minimum value that allows that voltage.
        voltage : voltage limit in V
        '''
        self.set_channel()
        #Need to add voltage level check for supplies that have voltage ranges
        #Need to have error for voltages that are too high as well
        self.comm(f'VOLT {voltage}, (@{self.channel})')

    def get_voltage(self):
        '''
        Returns the voltage limit in V
        '''
        self.set_channel()
        return float(self.comm(f'VOLT? (@{self.channel})'))

    def meas_voltage(self):
        '''
        Returns the measured voltage from the device in V
        '''
        self.set_channel()
        return float(self.comm(f'MEAS:VOLT? (@{self.channel})'))

    def set_out_state(self, state):
        '''
        Sets the output state
        state : boolean or 1/0
        '''
        self.set_channel()
        if state:
            self.comm(f'OUTP ON, (@{self.channel})')
        else:
            self.comm(f'OUTP OFF, (@{self.channel})')

    def get_out_state(self):
        '''
        Returns the output state
        '''
        self.set_channel()
        return int(self.comm(f'OUTP? (@{self.channel})'))