from cInst import cInst
from tkinter import ttk
from tkinter import *

class cInst_daq(cInst):
    '''
    daq main class
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'daq'
        self.channel_labels = []
        self.channel_values = []
        self.channel_units = []

    def _window_setup(self, root):
        self.root = root
        ttk.Label(root, text="Default cInst GUI").grid(column=0, row=0, pady=30, padx=30, columnspan=2)
        ttk.Button(root, text="Identify", command=self.gui_identify).grid(column=2, row=0)
        #Comm
        ttk.Label(root, text='Comm: ').grid(column=0, row=1, pady=30, padx=30)
        self.comm_text = Text(root, height=1, width=20)
        self.comm_text.grid(column=1, row=1)
        ttk.Button(root, text="Send", command=self.gui_comm).grid(column=2, row=1, pady=30, padx=30)
        ttk.Label(root, text='Return: ').grid(column=0, row=2, pady=30, padx=30)
        self.comm_return = ttk.Label(root, text='')
        self.comm_return.grid(column=1, row=2, pady=30, padx=30)
        #DAQ
        ttk.Label(root, text="Number of Channels: ").grid(column=0, row=3, pady=30, padx=30)
        self.num_channels = Text(root, height=1, width=10)
        self.num_channels.grid(column=1, row=3)
        self.num_channels.bind('<FocusOut>', self.update_channels)
        ttk.Button(root, text="Measure", command=self.gui_meas_voltage).grid(column=2, row=3)
        ttk.Label(root, text="Channel").grid(column=0, row=4, pady=30, padx=30)
        ttk.Label(root, text="Value").grid(column=1, row=4, pady=30, padx=30)
        ttk.Label(root, text="Units").grid(column=2, row=4, pady=30, padx=30)

    def update_channels(self, *args):
        #remove previous labels
        for label in self.channel_labels:
            label.destroy()
        for value in self.channel_values:
            value.destroy()
        for unit in self.channel_units:
            unit.destroy()

        try:
            num_channels = int(self.num_channels.get("1.0", "end"))
        except:
            print('Need int')

        self.channel_labels = []
        self.channel_values = []
        self.channel_units = []
        for i in range(num_channels):
            temp_label = ttk.Label(self.root, text=f'{i+1}')
            temp_label.grid(column=0, row=i+5, pady=30, padx=30)
            self.channel_labels.append(temp_label)
            temp_label = ttk.Label(self.root, text='')
            temp_label.grid(column=1, row=i+5, pady=30, padx=30)
            self.channel_values.append(temp_label)
            temp_label = ttk.Label(self.root, text="V")
            temp_label.grid(column=2, row=i+5, pady=30, padx=30)
            self.channel_units.append(temp_label)

        self.gui_meas_voltage()



    def gui_meas_voltage(self):
        try:
            num_channels = int(self.num_channels.get("1.0", "end"))
        except:
            print('Need int')

        for i in range(num_channels):
            measurement = str(self.meas_voltage(i+1))
            self.channel_values[i].config(text=measurement)#text=f'{float(measurement):.2f}')

    def meas_voltage(self, channel=1, magnitude = -3):
        return float(self.inst.query(f"MEAS:VOLT:DC? 10,{10**magnitude},(@{100+channel})"))


