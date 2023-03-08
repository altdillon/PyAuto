from cInst import cInst

class cInst_VNA(cInst):
    ''' 
    Vector Network Analyzer main class 
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'vector network analyzer' 

    # basic VNA functions.  Nothing special

    def set_sweep_time(self,sweep_time):
        '''Sets the seep time'''
        pass

    def set_sweep_time_auto(self):
        '''Set the sweep time to auto'''
        pass

    def set_freq(self,center=None,span=None,start=None,stop=None):
        '''Set the bandwidth of the VNA'''
        pass

    def set_points(self,points):
        '''Set the data points that the VNA measures'''

    def set_db_per_division(self,dvbis=10):
        '''Set the dB's per division'''

    def set_db_refrence(self,dbref=0):
        '''Set the refrence db'''

    def set_cw_freqency(self,cwfreq):
        '''Set the continous wave freqency'''

    # functions for getting S paramaters

    def get_single_s_params(self,sparam=None):
        '''get a single S parmater'''

    def get_s_params(self,sparam=None):
        '''return the first 4 s-pramaters'''

    # functions for setting RF power

    def toggle_rf_power(self,powerOn=True)
        '''turn the rf power on or off'''

    def get_rf_power(self):
        '''return the RF power in dBm'''
    
    def set_rf_power(self,powerLevel=0):
        '''set the RF power'''
    

    # TODO: Add functions for calibration