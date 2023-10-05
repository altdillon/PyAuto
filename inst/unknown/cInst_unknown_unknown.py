from cInst import cInst

class cInst_unknown_unknown(cInst):
    '''
    unknown main class
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'unknown'
