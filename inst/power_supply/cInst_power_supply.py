from cInst import cInst, pyauto_cInst_gui
from tkinter import ttk
from tkinter import *

class cInst_power_supply(cInst):
    '''
    power supply main class
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'power_supply'

    def window_setup(self, root):
        ttk.Label(root, text="Default Power Supply GUI").grid(column=0, row=0, pady=30, padx=30, columnspan=3)
        #Comm setup
        self.comm_label = ttk.Label(root, text='Comm: ')
        self.comm_label.grid(column=0, row=1, pady=30, padx=30)
        self.comm_text = Text(root, height=1, width=20)
        self.comm_text.grid(column=1, row=1)
        self.comm_button = ttk.Button(root, text="Send", command=self.gui_comm)
        self.comm_button.grid(column=2, row=1, pady=30, padx=30)
        self.comm_return_label = ttk.Label(root, text='Return: ')
        self.comm_return_label.grid(column=0, row=2, pady=30, padx=30)
        self.comm_return = ttk.Label(root, text='')
        self.comm_return.grid(column=1, row=2, pady=30, padx=30)


    def set_channel(self):
        '''
        dummy set channel for supplies that have multiple channels
        '''
        pass

    def set_current(self, current):
        '''
        Sets the current limit. Will error if current is set above the supply's capabilities. Set voltage prior to setting current limit
        current : current limit in A
        '''
        self.set_channel()
        #Add error handling (see voltage)
        self.comm(f'CURR {current}')

    def get_current(self):
        '''
        Returns the current limit in A
        '''
        self.set_channel()
        return float(self.comm('CURR?'))

    def meas_current(self):
        '''
        Returns the measured current from the device in A
        '''
        self.set_channel()
        return float(self.comm('MEAS:CURR?'))

    def set_voltage(self, voltage):
        '''
        Sets the voltage limit. Will adjust the voltage range (if applicable) to the minimum value that allows that voltage.
        voltage : voltage limit in V
        '''
        self.set_channel()
        #Need to add voltage level check for supplies that have voltage ranges
        #Need to have error for voltages that are too high as well
        self.comm(f'VOLT {voltage}')

    def get_voltage(self):
        '''
        Returns the voltage limit in V
        '''
        self.set_channel()
        return float(self.comm('VOLT?'))

    def meas_voltage(self):
        '''
        Returns the measured voltage from the device in V
        '''
        self.set_channel()
        return float(self.comm('MEAS:VOLT?'))

    def get_power(self):
        """
        Returns the maximum output power = V(limit) * I(limit)
        """
        self.set_channel()
        return self.get_voltage() * self.get_current()

    def meas_power(self):
        """
        Returns the output power = V * I
        """
        self.set_channel()
        return self.meas_voltage() * self.meas_current()

    def set_out_state(self, state):
        '''
        Sets the output state
        state : boolean or 1/0
        '''
        self.set_channel()
        if state:
            self.comm('OUTP ON')
        else:
            self.comm('OUTP OFF')

    def get_out_state(self):
        '''
        Returns the output state
        '''
        self.set_channel()
        return int(self.comm('OUTP?'))
    