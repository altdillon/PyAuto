from cInst_VNA import cInst_VNA
import re

class cInst_P5026A(cInst_VNA):
    '''
    Wrapper for the keysight P5026A skeysight Streamline USB vector
    Network analyzer.  This is a VNA with an intigrated spectrum Analyzer
    That has a bandwith from DC to 32 GHz
    '''

    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)

    

    def set_sweep_time(self,sweep_time):
        '''Sets the seep time'''
        if sweep_time is not None:
            self.comm(f'SENS:SWE:TIME {sweep_time}')
        pass

    def set_sweep_time_auto(self,auto=None):
        # set the sweep time to auto
        if auto is None: 
            isauto = self.comm('SENS:SWE:TIME:AUTO?')
            return isauto
        else:
            if auto is True:
                self.comm('SENS:SWE:TIME:AUTO YES')
            else:
                self.comm('SENS:SWE:TIME:AUTO NO')

    def set_if_bandwidth(self, ifbw, meas=1):
        self.comm(f'SENSe{meas}:BANDwidth {ifbw}')

    def set_freq(self,center=None,span=None,start=None,stop=None):
        '''Set the bandwidth of the VNA'''
        if center is not None and span is not None:
            self.comm(f'SENS:FREQ:CENT {center}') # set the center
            self.comm(f'SENS:FREQ:SPAN {span}') # set the span
        elif start is not None and stop is not None:
            # send stop and start.  Start is sent before stop
            self.comm(f'SENS:FREQ:STOP {stop}')
            self.comm(f'SENS:FREQ:STAR {start}')
        pass

    def set_points(self,points=101):
        '''Set the data points that the VNA measures'''
        if points > 0: # do some basic validation
            self.comm(f'SENS:SWE:POIN {points}')


    def set_db_per_division(self,dvbis=10):
        '''Set the dB's per division'''
        self.comm(f'DISP:MEAS:Y:PDIV {dvbis}')

    def set_db_refrence(self,dbref=0):
        '''Set the refrence db'''
        self.comm(f'DISP:MEAS:Y:RLEV {dbref}')

    def set_cw_freqency(self,cwfreq):
        '''Set the continous wave freqency'''
        pass # may not need this for the time being 

    # basicly a private reason to pull in a single S pramater plot
    def get_single_s_params(self,sparam=None):
        '''return the first 4 s-pramaters'''
        spram_regex = r'^S[0-9][0-9]'
        # validate the s paramater
        matches = re.findall(spram_regex,sparam)
        # if len(matches) == 1:
        #     self.comm('SYST:FPR') # get rid of the defult measument
        #     self.comm('DISP:WIND1:STAT ON') # create and turn on window 1
        #     self.comm(f'CALC1:MEAS1:DEF \'{sparam}\'') # set the measument
        #     self.comm('DISP:MEAS1:FEED 1') # display measument in window 1 and add a trace to it
        #     self.comm('CALC1:PAR:MNUM 1')
        #     self.comm('SENS1:SWE:TYPE LIN')
        #     # do a single sweep and return the results 
        #     self.comm('SENS1:SWE:MODE SING')    
        #     opcCode = self.comm('*OPC?')
        #     # return the stimuls and formatted responce data
        #     results = self.comm('CALC1:MEAS1:DATA:FDATA?')
        #     xValues = self.comm('CALC1:MEAS1:X:VAL?')
        #     # now that everything is all said and done go and return that
        #     return (xValues,results)

    def toggle_rf_power(self,powerOn=True):
        '''set the RF power'''
        if powerOn == True:
            self.comm('OUTP ON')
        else:
            self.comm('OUTP OFF')

    def set_rf_power(self,powerLevel=0):
        self.comm(f'SOUR:POW1 {powerLevel}')