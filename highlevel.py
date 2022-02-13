'''This will contain the main functions that can be used in automation. 
Nothing will be GUI related, but these functions will be used/available in the GUI'''

import os
import pyvisa
import clr
clr.AddReference('ModularZT_NET45')
from ModularZT_NET45 import USB_ZT

### Builds the lists containing the library content
dirname = os.path.dirname(os.path.abspath(__file__))

inst_library = {}
for directory in os.listdir(os.path.join(dirname, 'inst')):
	if os.path.isdir(directory):
		exec(f'inst_library[{directory}] = [f[6:-3] for f in os.listdir({directory}) if "cInst" in f]')

list_all_resources = []
for item,key in inst_library:
	list_all_resources.extend(item)

'''
list_power_supply = [f[6:-3] for f in os.listdir(os.path.join(dirname, 'inst', 'power_supply')) if "cInst" in f]
list_signal_generator = [f[6:-3] for f in os.listdir(os.path.join(dirname, 'inst', 'signal_generator')) if "cInst" in f]
list_arbitrary_waveform_generator = [f[6:-3] for f in os.listdir(os.path.join(dirname, 'inst', 'arbitrary_waveform_generator')) if "cInst" in f]
list_meter = [f[6:-3] for f in os.listdir(os.path.join(dirname, 'inst', 'meter')) if "cInst" in f]
list_temperature_chamber = [f[6:-3] for f in os.listdir(os.path.join(dirname, 'inst', 'temperature_chamber')) if "cInst" in f]
list_frequency_counter = [f[6:-3] for f in os.listdir(os.path.join(dirname, 'inst', 'frequency_counter')) if "cInst" in f]
list_oscilloscope = [f[6:-3] for f in os.listdir(os.path.join(dirname, 'inst', 'oscilloscope')) if "cInst" in f]
list_relay = [f[6:-3] for f in os.listdir(os.path.join(dirname, 'inst', 'relay')) if "cInst" in f]
list_spectrum_analyzer = [f[6:-3] for f in os.listdir(os.path.join(dirname, 'inst', 'spectrum_analyzer')) if "cInst" in f]
list_phase_noise_analyzer = [f[6:-3] for f in os.listdir(os.path.join(dirname, 'inst', 'phase_noise_analyzer')) if "cInst" in f]
list_all_resources = list_power_supply+list_signal_generator+list_arbitrary_waveform_generator+list_meter+list_temperature_chamber+list_frequency_counter+list_oscilloscope+list_relay+list_spectrum_analyzer+list_phase_noise_analyzer
'''

class Bench():
	'''This class represents the bench that is hooked up to the computer. It will be created by the "scan_bench" function.'''
	def __init__(self,dict_inst):
		self.power_supply = dict_inst['power_supply']
		self.signal_generator = dict_inst['signal_generator']
		self.temperature_chamber = dict_inst['temperature_chamber']
		self.meter = dict_inst['meter']
		self.arbitrary_waveform_generator = dict_inst['arbitrary_waveform_generator']
		self.frequency_counter = dict_inst['frequency_counter']
		self.oscilloscope = dict_inst['oscilloscope']
		self.spectrum_analyzer = dict_inst['spectrum_analyzer']
		self.phase_noise_analyzer = dict_inst['phase_noise_analyzer']
		self.relay = dict_inst['relay']
		self.unknown = dict_inst['unknown']

	def launch_gui():
		'''this will launch the "Bench" GUI. It will give access to the things with in Bench like the instrument GUIs'''
		pass



def scan_bench(TCPIP_addresses = [], do_USB = True, do_GPIB = True):
    """
    Scans all the connected instruments to the PC and initializes the appropriate class
    gd = globals() to allow a global scope to the instruments
    do_USB      = True/False     Scan USB connected instruments
    do_TCPIP    = True/False     Scan LAN connected instruments
    do_GPIB     = True/False     Scan GPIB connected instruments
    """
    
    g_resource = []; u_resource = []; t_resource = []; resource_to_open = []

    dict_available_inst = {	'power_supply':					[],
    						'signal_generator':				[],
    						'temperature_chamber':			[],
    						'meter':						[],
    						'arbitrary_waveform_generator':	[],
    						'frequency_counter':			[],
    						'oscilloscope':					[],
    						'spectrum_analyzer':			[],
    						'phase_noise_analyzer':			[],
    						'relay':						[],
    						'unknown':						[]}
    
    print('Scanning all instruments...', end="\n\n")
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
		mc_relays_possible_sn = list(mc_relays.Get_Available_SN_List("")[1].split(" "))
        resource_to_open.extend(mc_relays_possible_sn) 
    if len(TCPIP) > 0:
    	for r in t_resource:
    		if any(TCPIP_address in r for TCPIP_address in TCPIP_addresses)
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

        #Added this part to support AirJet and Relay with unconventional names
        if gid == 'Inc.':
            gid = temp.query('*IDN?').split(',')[2].replace(' ','')
        elif gid == '3.0':
            gid = temp.query('*IDN?').split(',')[0].replace('-','')
            
        

        class_name = 'cInst_' + gid
        if class_name in list_all_resources:



'''need to add imports'''



        class_name = 'cInst_' + gid
        if gid in list_power_supply:
            if gid == "E3631A":
                for p in [1,2,3]:
                    dict_inst['power_supply'].append(eval(f'lib.instr.PowSup.{class_name}_{p}.{class_name}_{p}(temp)'))
            elif gid == "E3646A":
                for p in [1,2]:
                    dict_inst['power_supply'].append(eval(f'lib.instr.PowSup.{class_name}_{p}.{class_name}_{p}(temp)'))
            else:
                dict_inst['power_supply'].append(eval('lib.instr.PowSup.{}.{}(temp)'.format(class_name,class_name)))
        elif gid in list_SigGen:
            SigGen.append(eval('lib.instr.SigGen.{}.{}(temp)'.format(class_name,class_name)))
            print(f"Determined type as Signal Generator. Assigning to SigGen", end="\n\n")
        elif gid in list_TempCh:
            TempCh.append(eval('lib.instr.TempCh.{}.{}(temp)'.format(class_name,class_name)))
            print(f"Determined type as Temperature Chamber. Assigning to TempCh", end="\n\n")
        elif gid in list_Meter:
            Meter.append(eval('lib.instr.Meter.{}.{}(temp)'.format(class_name,class_name)))
            print(f"Determined type as Digital Multimeter. Assigning to Meter", end="\n\n")
        elif gid in list_ArbGen:
            ArbGen.append(eval('lib.instr.ArbGen.{}.{}(temp)'.format(class_name,class_name)))
            print(f"Determined type as Arbitrary Waveform Generator. Assigning to ArGen", end="\n\n")
        elif gid in list_FreqCntr:
            FreqCntr.append(eval('lib.instr.FreqCntr.{}.{}(temp)'.format(class_name,class_name)))
            print(f"Determined type as Frequency Counter. Assigning to FreqCntr", end="\n\n")
        elif gid in list_SpecAn:
            SpecAn.append(eval('lib.instr.SpecAn.{}.{}(temp)'.format(class_name,class_name)))
            print(f"Determined type as Spectrum Analyzer. Assigning to SpecAn", end="\n\n")
        elif gid in list_PNA:
            PNA.append(eval('lib.instr.PNA.{}.{}(temp)'.format(class_name,class_name)))
            print(f"Determined type as Phase Noise Analyzer. Assigning to PNA", end="\n\n")
        elif gid in list_Oscope:
            Oscope.append(eval('lib.instr.Oscope.{}.{}(temp)'.format(class_name,class_name)))
            print(f"Determined type as Oscilloscope. Assigning to Oscope", end="\n\n")
        elif gid in list_Relay:
            Relay.append(eval('lib.instr.Relay.{}.{}(temp)'.format(class_name,class_name)))
            print(f"Determined type as Relay Box. Assigning to Relay", end="\n\n")
        else:
            class_name = 'cInst_Unknown'
            Unknown.append(eval('lib.instr.Unknown.{}.{}(temp)'.format(class_name,class_name)))
            print(f"Could not determine type. Assigning to Unknown", end="\n\n")
        
    
    # List of all assigned instruments
    assigned_instr = ArbGen + Dscope + FreqCntr + Meter + Oscope + PNA + PowSup + Relay + SigGen + SpecAn + TempCh + Unknown + Troubled
    gd['TempCh'] = TempCh; gd['PowSup'] = PowSup; gd['SigGen'] = SigGen; gd['ArbGen'] = ArbGen; 
    gd['PNA'] = PNA; gd['Meter'] = Meter; gd['FreqCntr'] = FreqCntr; gd['SpecAn'] = SpecAn; 
    gd['Oscope'] = Oscope; gd['Dscope'] = Dscope; gd['Relay'] = Relay; gd['Unknown'] = Unknown
    gd["Troubled"] = Troubled
    
    # Printing all instruments and GPIB Addresses
    char_length = 100
    print('')
    print("="*char_length)
    print("THIS BENCH".center(char_length))
    print("-"*char_length)

    for instrument in assigned_instr:
        print('{}[{}]'.format(instrument.type,eval('{}.index(instrument)'.format(instrument.type))).ljust(15,' '), end = '\t')
        print(f"Comm = {instrument.get_connection_mode().ljust(5)}| Address = {instrument.get_address().ljust(18)}", end="\t")
        if instrument.type != "Troubled":
            print('Model: '.rjust(7),instrument.name.ljust(30))
        else:
            print('Model: '.rjust(7),"No response".ljust(30))

 
    print("="*char_length)
    print('')
    print('Unavailable but connected Instruments')
    print('='*char_length)
    print('TCP/IP Instruments'.ljust(15))
    if not do_TCPIP:
        print(t_resource)
    print('-'*int(char_length/2))
    print('USB Instruments'.ljust(15))
    if not do_USB:
        print(u_resource)
    print('-'*int(char_length/2))

