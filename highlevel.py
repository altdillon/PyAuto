'''This will contain the main functions that can be used in automation. 
Nothing will be GUI related, but these functions will be used/available in the GUI'''

import os

### Builds the lists containing the library content
dirname = os.path.dirname(os.path.abspath(__file__))

inst_library = {}
for directory in os.listdir(os.path.join(dirname, 'inst')):
    if os.path.isdir(os.path.join(dirname, 'inst', directory)) and directory != '__pycache__':
        exec(f'inst_library["{directory}"] = [f[6:-3] for f in os.listdir(r"{os.path.join(dirname, "inst", directory)}") if "cInst" in f]')

class Bench():
    '''This class represents the bench that is hooked up to the computer. It will be created by the "scan_bench" function.'''
    def __init__(self,dict_inst):
        for instrument_type,instrument_list in dict_inst.items():
            if len(instrument_list) > 0:
                exec(f'self.{instrument_type} = instrument_list')

    def launch_gui(self):
        '''this will launch the "Bench" GUI. It will give access to the things with in Bench like the instrument GUIs'''
        pass

def launch_gui():
    pass

def scan_bench(TCPIP_addresses = [], do_USB = True, do_GPIB = True):
    """
    Scans all the connected instruments to the PC and initializes the appropriate class
    returns Bench class
    TCPIP_addresses	= List 			Connect LAN instruments listed
    do_USB      	= True/False    Scan USB connected instruments
    do_GPIB     	= True/False    Scan GPIB connected instruments
    """
    
    import pyvisa
    from .lowlevel import instantiate_inst
    import clr
    clr.AddReference(os.path.join(dirname, 'inst', 'relay', 'ModularZT_NET45.dll'))
    from ModularZT_NET45 import USB_ZT
    g_resource = []; u_resource = []; t_resource = []; resource_to_open = []

    dict_available_inst = {	'power_supply':			[],
                                'signal_generator':		[],
                                'temperature_chamber':		[],
                                'meter':			[],
                                'arbitrary_waveform_generator':	[],
                                'frequency_counter':		[],
                                'oscilloscope':			[],
                                'spectrum_analyzer':		[],
                                'phase_noise_analyzer':		[],
                                'relay':			[],
                                'unknown':			[]}
    
    #print('Scanning all instruments...', end="\n\n")
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
        mc_relays = USB_ZT()
        if mc_relays.Get_Available_SN_List("")[0] > 0:
            mc_relays_possible_sn = list(mc_relays.Get_Available_SN_List("")[1].split(" "))
            resource_to_open.extend(mc_relays_possible_sn)
    if len(TCPIP_addresses) > 0:
        for r in t_resource:
            if any(TCPIP_address in r for TCPIP_address in TCPIP_addresses):
                resource_to_open.apeend(r)
    if do_GPIB:
        resource_to_open.extend(g_resource)
    
    for g in resource_to_open:
        if g[:3] not in ["GPI","USB","TCP","ASL"]:
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
                dict_available_inst[instrument_type].extend(instantiate_inst(gid, temp, connection_mode))

        if unknown:
            dict_available_inst['unknown'].append(instantiate_inst('unknown', temp, connection_mode))


    return Bench(dict_available_inst)
