from cInst import cInst

class cInst_signal_generator(cInst):
    '''
    signal generator main class
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'signal_generator'
