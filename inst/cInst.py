class cInst:
    '''
    Master Instrument class which abstracts pyvisa
    '''
    
    def __init__(self,inst, inst_id, connection_mode, address):
        self.inst = inst
        self.id = inst_id
        self.connection_mode = connection_mode
        self.address = address
        
    def comm(self,command):
        if '?' in command:
            return self.inst.query(command)
        else:
            return self.inst.write(command)

    def set_address(self, address):
        pass

    def launch_gui(self):
        pass

    def reset(self):
        self.comm('*RST')

    def disconnect(self):
        self.inst.close()
