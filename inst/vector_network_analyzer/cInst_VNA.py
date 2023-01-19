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
