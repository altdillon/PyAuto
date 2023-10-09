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

    def _window_setup(self, root):
        ttk.Label(root, text="Default cInst GUI").grid(column=0, row=0, pady=30, padx=30, columnspan=2)
        ttk.Button(root, text="Identify", command=self.gui_identify).grid(column=2, row=0)
        #DAQ
        ttk.Label(root, text="Number of Channels: ").grid(column=0, row=1, pady=30, padx=30)
        self.num_channels = Text(root, height=1, width=10)
        self.num_channels.grid(column=1, row=1)
        ttk.Label(root, text="Channel").grid(column=0, row=2, pady=30, padx=30)
        ttk.Label(root, text="Value").grid(column=1, row=2, pady=30, padx=30)
        ttk.Label(root, text="Units").grid(column=2, row=2, pady=30, padx=30)
        #Comm
        ttk.Label(root, text='Comm: ')grid(column=0, row=1, pady=30, padx=30)
        self.comm_text = Text(root, height=1, width=20)
        self.comm_text.grid(column=1, row=1)
        ttk.Button(root, text="Send", command=self.gui_comm).grid(column=2, row=1, pady=30, padx=30)
        ttk.Label(root, text='Return: ').grid(column=0, row=2, pady=30, padx=30)
        self.comm_return = ttk.Label(root, text='')
        self.comm_return.grid(column=1, row=2, pady=30, padx=30)
