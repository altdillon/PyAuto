'''This will contain the main functions that can be used in automation. 
Nothing will be GUI related, but these functions will be used/available in the GUI'''

import os
import platform
import tkinter
from tkinter import ttk
from tkinter import *

### Builds the lists containing the library content
dirname = os.path.dirname(os.path.abspath(__file__))

inst_library = {}
for directory in os.listdir(os.path.join(dirname, 'inst')):
    if os.path.isdir(os.path.join(dirname, 'inst', directory)) and directory != '__pycache__':
        exec(f'inst_library["{directory}"] = [f.split("_")[1] for f in os.listdir(r"{os.path.join(dirname, "inst", directory)}") if "cInst" in f]')


class Bench():
    '''This class represents the bench that is hooked up to the computer. It will be created by the "scan_bench" function.'''
    def __init__(self):
        self.gui = None

    def __iter__(self):
        return iter(self.equipment_list)

    #eventually make gui functions inaccessable to users
    def on_window_close(self):
        self.gui.destroy()
        self.gui = None


    def scan_bench(self, TCPIP_addresses = [], do_USB = True, do_GPIB = True):
        """
        Scans all the connected instruments to the PC and initializes the appropriate class
        returns Bench class
        TCPIP_addresses	= List 			Connect LAN instruments listed
        do_USB      	= True/False    Scan USB connected instruments
        do_GPIB     	= True/False    Scan GPIB connected instruments
        """
        
        import pyvisa
        from .lowlevel import instantiate_inst
        if platform.system() == 'Windows': # this will only work under windows
            import clr
            clr.AddReference(os.path.join(dirname, 'inst', 'relay', 'ModularZT_NET45.dll'))
            from ModularZT_NET45 import USB_ZT
        import ctypes, ctypes.util
        g_resource = []; u_resource = []; t_resource = []; resource_to_open = []

        dict_available_inst = {}
        for directory in os.listdir(os.path.join(dirname, 'inst')):
            if os.path.isdir(os.path.join(dirname, 'inst', directory)) and directory != '__pycache__':
                dict_available_inst[directory] = []
        
        #print('Scanning all instruments...', end="\n\n")
        # get a list of possible visa devices 
        rm = pyvisa.ResourceManager()
        all_resource = rm.list_resources()
        
        for r in all_resource:
            if 'GPIB' in r:
                g_resource.append(r)
            elif 'USB' in r:
                u_resource.append(r)
            elif 'TCP' in r:
                t_resource.append(r)

        if do_USB:
            resource_to_open.extend(u_resource)

            #relays
            mc_relays = USB_ZT()
            if mc_relays.Get_Available_SN_List("")[0] > 0:
                mc_relays_possible_sn = list(mc_relays.Get_Available_SN_List("")[1].split(" "))
                resource_to_open.extend(mc_relays_possible_sn)

            #pico scopes
            _libps6000 = ctypes.WinDLL(os.path.join(dirname, 'inst', 'oscilloscope', 'ps6000.dll'))       #ctypes.util.find_library("ps6000"))
            count = ctypes.c_int16()
            length = ctypes.c_int16(640)
            serials = ctypes.create_string_buffer(length.value)
            _libps6000["ps6000EnumerateUnits"](ctypes.byref(count), serials, ctypes.byref(length))
            if count.value > 0:
                resource_to_open.extend(serials.value.decode().split(','))

        if len(TCPIP_addresses) > 0:
            if TCPIP_addresses[0] == '*':
                resource_to_open.extend(t_resource)
            else:
                for r in t_resource:
                    if any(TCPIP_address in r for TCPIP_address in TCPIP_addresses):
                        resource_to_open.apeend(r)
        
        if do_GPIB:
            resource_to_open.extend(g_resource)
        
        for g in resource_to_open:
            if g[:3] not in ["GPI","USB","TCP","ASL"]:
                if '/' in g: #hopefully only/all pico
                    temp = ctypes.c_int16(0)
                    _libps6000["ps6000OpenUnit"](ctypes.byref(temp), ctypes.c_char_p(g.encode()))
                    line = ctypes.create_string_buffer(64)
                    required = ctypes.c_int16()
                    _libps6000["ps6000GetUnitInfo"](temp, line, ctypes.c_int16(64), ctypes.byref(required), ctypes.c_uint32(0x00000003))
                    gid = "ps" + line.value.decode()
                else:
                    mc_relays.Connect(g)
                    gid = mc_relays.Read_ModelName("")[1].replace("-","_")
                    temp = g
            else:
                temp = rm.open_resource(g)
                try:
                    gid = temp.query('*IDN?').split(',')[1]
                except:
                    try:
                        gid = temp.query('*ID?').split(',')[1]
                    except:
                        try:
                            gid = temp.query('ID?').split(',')[1]
                        except:
                            try:
                                gid = temp.query('ID').split(',')[1]
                            except:
                                gid = g

            gid = gid.replace(' ','')
            gid = gid.replace('-','')
            gid = gid.replace('\n','')
            gid = gid.replace('_','')

            if g in g_resource:
                connection_mode = 'GPIB'
            elif g in t_resource:
                connection_mode = 'TCPIP'
            else:
                connection_mode = 'USB'

            #Added this part to support AirJet and Relay with unconventional names
            if gid == 'Inc.':
                gid = temp.query('*IDN?').split(',')[2].replace(' ','')
            elif gid == '3.0':
                gid = temp.query('*IDN?').split(',')[0].replace('-','')
                
            unknown = True
            for instrument_type,instrument_list in inst_library.items():
                if gid in instrument_list:
                    unknown = False
                    dict_available_inst[instrument_type].extend(instantiate_inst(gid, temp, connection_mode, unknown, instrument_type))

            if unknown:
                dict_available_inst['unknown'].extend(instantiate_inst(gid, temp, connection_mode, unknown, 'unknown'))

        #return Bench(dict_available_inst)
        self.equipment_list = []
        for instrument_type,instrument_list in dict_available_inst.items():
            self.equipment_list += instrument_list
            if len(instrument_list) > 0:
                exec(f'self.{instrument_type} = instrument_list')

def launch_gui():
    pyauto_gui()

class pyauto_gui():
    def __init__(self):
        self.b = Bench()

        self.root = tkinter.Tk()
        self.root.title("pyauto")
        self.root.wm_iconbitmap(os.path.join(dirname, "example_icon.ico"))

        ttk.Label(self.root, text="Select the communication standards and scan the bench to start").grid(column=0, row=0, pady=30, padx=30, columnspan=3)
        self.TCPIP = IntVar()
        Checkbutton(self.root, text="TCPIP", variable=self.TCPIP, command=self.show_TCPIP).grid(column=0, row=1)
        self.USB = IntVar()
        Checkbutton(self.root, text="USB", variable=self.USB).grid(column=1, row=1)
        self.GPIB = IntVar()
        Checkbutton(self.root, text="GPIB", variable=self.GPIB).grid(column=2, row=1)
        self.scan_bench_button = ttk.Button(self.root, text="Scan Bench", command=self.scan_and_open)
        self.scan_bench_button.grid(column=0, row=2, pady=30, padx=30, columnspan=3)

        self.root.attributes('-topmost',1)
        self.root.attributes('-topmost',0)

        self.root.mainloop()

    def scan_and_open(self):
        if self.b.gui == None:
            if self.TCPIP.get():
                tcpip_text = self.TCPIP_addresses.get("1.0", "end").strip()
                if len(tcpip_text) > 0:
                    tcpip_addresses = tcpip_text.split(',')
                else:
                    tcpip_addresses = ['*']
            else:
                tcpip_addresses = []
            self.b.scan_bench(TCPIP_addresses = tcpip_addresses, do_USB = self.USB.get(), do_GPIB = self.GPIB.get())
            self.b.gui = pyauto_bench_gui(self.b, self.root)
        else:
            self.b.gui.lift()

    def show_TCPIP(self):
        if self.TCPIP.get():
            #showing
            self.TCPIP_label = ttk.Label(self.root, text="TCPIP Addresses (Leave blank if all devices)")
            self.TCPIP_label.grid(column=0, row=2)
            self.TCPIP_addresses = Text(self.root, height=1, width=20)
            self.TCPIP_addresses.grid(column=1, row=2, columnspan=2, pady=30, padx=30)
            self.scan_bench_button.grid(column=0, row=3, pady=30, padx=30, columnspan=3)
        else:
            self.TCPIP_label.grid_remove()
            self.TCPIP_addresses.grid_remove()
            self.scan_bench_button.grid(column=0, row=2, pady=30, padx=30, columnspan=3)
        

class pyauto_bench_gui(tkinter.Toplevel):
    def __init__(self, bench, root):
        self.bench = bench
        super().__init__(root)
        self.title("pyauto_bench")
        self.wm_iconbitmap(os.path.join(dirname, "example_icon.ico"))

        self.protocol("WM_DELETE_WINDOW", self.bench.on_window_close)

        list_labels = []
        for inst in self.bench:
            if inst.type not in list_labels:
                list_labels.append(inst.type)

        if len(list_labels) == 0:
            ttk.Label(self, text='No Instruments Found').grid(column=0, row=0, pady=30, padx=30)
        else:
            ttk.Label(self, text='Select the instrument to launch its GUI').grid(column=0, row=0, pady=30, padx=30, columnspan=len(list_labels))

            for i in range(len(list_labels)):
                ttk.Label(self, text=list_labels[i].upper()).grid(column=i, row=1, pady=30, padx=30)
                j=0
                for inst in eval(f'self.bench.{list_labels[i]}'):
                    ttk.Button(self, text=f'{list_labels[i]} {j}', command=lambda id_number=j, instrument=inst: instrument.launch_gui(id_number, root)).grid(column=i, row=2+j, pady=30, padx=30)
                    j+=1

        self.lift()

