from cInst_VNA import cInst_VNA

class cInst_NanoVNA(cInst_VNA):
    '''
    Nano VNA.  This is a very low cost, some would say cheap open source VNA
    Most versions can do 0 - 3 GHz.  It uses serial for communication
    '''
    def __init__(self, inst, inst_id, connection_mode, address, channel):
        super().__init__(inst, inst_id, connection_mode, address)