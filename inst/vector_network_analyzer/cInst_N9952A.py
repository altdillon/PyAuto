from cInst_VNA import cInst_VNA

class cInst_N9952A(cInst_VNA):
    '''
    Wrapper for the Keysight feild fox N9952A VNA
    This is a DC - 50 GHz hand held VNA devloped by keysight.
    It uses a the standard scipy/VISA as defined by keysight
    '''
    def __init__(self, inst, inst_id, connection_mode, address, channel):
        super().__init__(inst, inst_id, connection_mode, address)