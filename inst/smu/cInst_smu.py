from cInst import cInst

class cInst_smu(cInst):
    '''
    power supply main class
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'smu'