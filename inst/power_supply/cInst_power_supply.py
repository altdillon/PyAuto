from cInst import cInst

class cInst_power_supply(cInst):
    '''
    power supply main class
    '''

    def set_current(self, currrent):
        '''
        Sets the current limit. Will error if current is set above the supply's capabilities. Set voltage prior to setting current limit
        current : current limit in A
        '''
        #Add error handling (see voltage)
        self.comm(f'CURR {current}')

    def get_current(self):
        '''
        Returns the current limit in A
        '''
        return float(self.comm('CURR?'))

    def meas_current(self):
        '''
        Returns the measured current from the device in A
        '''
        return float(self.comm('MEAS:CURR?'))

    def set_voltage(self, voltage):
        '''
        Sets the voltage limit. Will adjust the voltage range (if applicable) to the minimum value that allows that voltage.
        voltage : voltage limit in V
        '''
        #Need to add voltage level check for supplies that have voltage ranges
        #Need to have error for voltages that are too high as well
        self.comm(f'VOLT {voltage}')

    def get_voltage(self):
        '''
        Returns the voltage limit in V
        '''
        return float(self.comm('VOLT?'))

    def meas_voltage(self):
        '''
        Returns the measured voltage from the device in V
        '''
        return float(self.comm('MEAS:VOLT?'))

    def get_power(self):
        """
        Returns the maximum output power = V(limit) * I(limit)
        """
        return self.get_voltage() * self.get_current()

    def meas_power(self):
        """
        Returns the output power = V * I
        """
        return self.meas_voltage() * self.meas_current()

    def set_out_state(self, state):
        '''
        Sets the output state
        state : boolean or 1/0
        '''
        if state:
            self.comm('OUTP ON')
        else:
            self.comm('OUTP OFF')

    def get_out_state(self):
        '''
        Returns the output state
        '''
        return int(self.comm('OUTP?'))
