from cInst import cInst

class cInst_temperature_chamber(cInst):
    '''
    temperature chamber main class
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'temperature_chamber'
