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

    def set_db_per_devision(self,db_devision):
        '''Sets the dB per devision'''
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

    def get_s_params(self):
        '''return the first 4 s-pramaters'''

    

    # TODO: Add functions for calibration