import tkinter
from tkinter import ttk
from tkinter import *
import os
import time

class cInst:
    '''
    Master Instrument class which abstracts pyvisa
    '''
    
    def __init__(self, inst, inst_id, connection_mode, address):
        self.inst = inst
        self.id = inst_id
        self.connection_mode = connection_mode
        self.address = address
        self.gui = None
        
    def comm(self, command):
        if '?' in command:
            return self.inst.query(command)
        else:
            self.inst.write(command)

    def set_address(self, address):
        pass

    def launch_gui(self, id_number, root):
        if self.gui == None:
            self.gui = pyauto_cInst_gui(self, id_number, root)
        else:
            self.gui.lift()

    def _window_setup(self, root):
        ttk.Label(root, text="Default cInst GUI").grid(column=0, row=0, pady=30, padx=30, columnspan=2)
        ttk.Button(root, text="Identify", command=self.gui_identify).grid(column=2, row=0)
        ttk.Label(root, text='Comm: ').grid(column=0, row=1, pady=30, padx=30)
        self.comm_text = Text(root, height=1, width=20)
        self.comm_text.grid(column=1, row=1)
        ttk.Button(root, text="Send", command=self.gui_comm).grid(column=2, row=1, pady=30, padx=30)
        ttk.Label(root, text='Return: ').grid(column=0, row=2, pady=30, padx=30)
        self.comm_return = ttk.Label(root, text='')
        self.comm_return.grid(column=1, row=2, pady=30, padx=30)

    def gui_comm(self):
        command = self.comm_text.get("1.0", "end").strip()
        query_return = self.comm(command)
        if query_return != None:
            self.comm_return.config(text = query_return.strip())
        else:
            self.comm_return.config(text = 'Sent!')

    def gui_identify(self, persist=False):
        if persist:
            self.comm('DISP:TEXT "ME"')
        else:
            for i in range(5):
                self.comm('DISP:TEXT "ME"')
                time.sleep(0.3)
                self.comm('DISP:TEXT:CLE')
                time.sleep(0.3)

    def on_window_close(self):
        self.gui.destroy()
        self.gui = None

    def reset(self):
        self.comm('*RST')

    def disconnect(self):
        self.inst.close()

class pyauto_cInst_gui(tkinter.Toplevel):
    def __init__(self, inst, id_number, root):
        self.inst = inst
        self.id_number = id_number
        super().__init__(root)

        self.protocol("WM_DELETE_WINDOW", self.inst.on_window_close)

        try:
            self.title(f"pyauto_{self.inst.type}_{self.id_number}")
        except:
            self.title("pyauto")
        self.wm_iconbitmap(os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], "Icon.ico"))

        self.inst._window_setup(self)

        self.lift()
        
