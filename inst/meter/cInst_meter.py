from cInst import cInst

class cInst_meter(cInst):
    '''
    meter main class
    '''
    def beep(self):
        '''
        Sounds a beep from the instrument. Useful if you want audio cues in a script
        '''
        self.comm('SYST:BEEP')

    def meas_dc_voltage(self):
        '''
        Returns a dc voltage measurement in V
        '''
        return float(self.comm('MEAS:VOLT:DC?'))
        
    def meas_ac_voltage(self):
        '''
        Returns a ac voltage measurement in V
        '''
        return float(self.comm('MEAS:VOLT:AC?'))

    def set_trigger(self, trigger):
        '''
        Sets the trigger for capturing data
        trigger : ['immediate', 'internal', 'external', 'bus']
        IMM --> always
        INT --> internal trigger. Not used
        EXT --> external trigger. Connect source behind
        BUS --> Triggers on commands like MEAS, READ, INIT
        '''
        if trigger.upper() in 'IMMEDIATE':
            self.comm('TRIG:SOUR IMM')
        elif trigger.upper() in 'INTERNAL':
            self.comm('TRIG:SOUR INT')
        elif trigger.upper() in 'EXTERNAL':
            self.comm('TRIG:SOUR EXT')
        elif trigger.upper() in 'BUS':
            self.comm('TRIG:SOUR BUS')
        else:
            raise ValueError("trigger must be one of the following: ['immediate', 'internal', 'external', 'bus']")

    def get_trigger(self):
        '''
        Returns the trigger source
        '''
        trigger = self.comm('TRIG:SOUR?')[:-1]
        if trigger.upper() in 'IMMEDIATE':
            return 'immediate'
        elif trigger.upper() in 'INTERNAL':
            return 'internal'
        elif trigger.upper() in 'EXTERNAL':
            return 'external'
        elif trigger.upper() in 'BUS':
            return 'bus'
        else:
            return 'unknown'