from cInst_power_supply import cInst_power_supply

def cInst_N6700C_power_supply(inst, inst_id, connection_mode, address):
    channels = int(inst.query('SYST:CHAN?'))
    ret = []
    for i in range(channels):
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