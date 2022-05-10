from cInst import cInst

class cInst_spectrum_analyzer(cInst):
    '''
    spectrum analyzer main class
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'spectrum_analyzer'
