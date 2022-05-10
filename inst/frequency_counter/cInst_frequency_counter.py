from cInst import cInst

class cInst_frequency_counter(cInst):
    '''
    frequency counter main class
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'frequency_counter'
