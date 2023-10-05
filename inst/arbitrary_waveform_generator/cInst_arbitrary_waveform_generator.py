from cInst import cInst

class cInst_arbitrary_waveform_generator(cInst):
    '''
    arbitrary waveform generator main class
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'arbitrary_waveform_generator'


    '''just copied below code'''





  
    def reset(self): 
        self.comm('*RST') 
        print('Reset to Factory defaults') 

    def set_pulse(self,period = 1e-6,width=0.5e-6,trans_time='MIN',v_high=1,v_low=0): 
        ''' 
        Configure the pulse parameters. trans_time = Rise/Fall time. Use 'MIN' for fastest edge 
        ''' 
        try: 
            self.set_wave_shape("PULS") 
        except: 
            self.comm("FUNC PULS") 
        if period < 2000: 
            per = max(20e-9,period) 
        else: 
            per = 2000 
        if width < 2000: 
            wid = max(8e-9,width) 
        else: 
            wid = 2000 
        if isinstance(trans_time,str): 
            tr = trans_time 
        else: 
            if trans_time < 1e-3: 
                tr = max(trans_time,5e-9) 
            else: 
                tr = 1e-3 
        self.comm('PULS:PER {}'.format(per)) 
        self.comm('PULS:WID {}'.format(wid)) 
        self.comm('PULS:TRAN {}'.format(tr)) 
        self.set_volt_vh_vl(v_high,v_low) 
        self.get_present_settings() 

    def set_pulse_width(self,pw): 
        if self.get_wave_shape() == 'PULS': 
            self.set_pulse(width=pw) 
            pw_set = float(self.comm("PULS:WID?")) 
            print(f"Pulse Width = {pw_set}") 
        else: 
            print('Instrument not in Pulse mode. use set_pulse first') 


    def set_square_wave(self,frequency = 10e6, v_high = 2, v_low = 0, duty_cycle = 50): 
        ''' 
        Configure a square wave 
        ''' 
        self.set_wave_shape('SQU') 
        self.set_volt_vh_vl(v_high,v_low) 
        self.set_frequency(frequency) 
        self.set_duty_cycle(duty_cycle) 
        #self.get_present_settings() 

    def set_sine_wave(self,frequency=1e6,v_pp=2,v_offset=1): 
        ''' 
        Configure sine waveform 
        ''' 
        self.set_frequency(frequency) 
        self.set_wave_shape('SIN') 
        self.set_volt_ampl_offs(v_pp,v_offset) 
        #self.get_present_settings() 

    def set_ramp(self,frequency=1e6,v_high=1, v_low=-1,symm=100): 
        ''' 
        Configures RAMP. symm=100 => zero crossing happens mid ramp 
        ''' 
        self.set_wave_shape('RAMP') 
        self.set_volt_vh_vl(v_high,v_low) 
        self.comm('FUNC:RAMP:SYMM {}'.format(symm)) 
        if frequency > 1e6: 
            freq = 1e6 
        else: 
            freq = min(1e6,frequency) 
        self.set_frequency(freq) 
        self.get_present_settings() 

    def set_noise(self,v_rms=0.1): 
        ''' 
        Sets noise with a v_rms specified value 
        ''' 
        self.set_volt_unit('VRMS') 
        self.set_out_quick('NOIS','DEF',v_rms,0) 
        self.get_present_settings() 

    def set_frequency(self,frequency = 10e6): 
        ''' 
        Sets waveform frequency 
        ''' 
        self.comm('FREQ {}'.format(frequency)) 

    def get_frequency(self): 
        return(float(self.comm('FREQ?'))) 


    def get_present_settings(self): 
        ''' 
        Read current waveform setting. Frequency may not be relevant in DC case 
        ''' 
        get_var1 = self.comm('APPLY?')[:-1].split(',') 
        get_var2 = get_var1[0].split(' ') 
        print('Wave_shape = ',get_var2[0]) 
        print('Frequency = {}KHz'.format(float(get_var2[1])/1e3)) 
        print('Vpp = {}{}'.format(get_var1[1].ljust(10),self.get_volt_unit()), end = '\t') 
        print('Voffset = {}V'.format(get_var1[2].ljust(10)))     


    def set_wave_shape(self,shape='SQUARE'): 
        ''' 
        Sets waveform shape only. You need to set other parameters based on wave shape 
        ''' 
        if shape[2] != None: 
            if shape[:2].upper() in 'SQUARE': 
                shape_var = 'SQU' 
            elif shape[:2].upper() in 'SINUSOID': 
                shape_var = 'SIN' 
            elif shape[:2].upper() in 'RAMP': 
                shape_var = 'RAMP'  
            elif shape[:2].upper() in 'NOISE': 
                shape_var = 'NOIS' 
            elif shape[:2].upper in "PULSE": 
                shape_var = 'PULS' 
            elif shape[:2].upper in 'DC': 
                shape_var = 'DC' 
            self.comm('FUNC {}'.format(shape_var)) 
            # print('----Waveform set----') 
            # print('Set other paramerter separately') 
        else: 
            print('Unknown shape {}'.format(shape)) 
            print("Choose one from 'SQU';'SIN';'RAMP';'NOIS';'PULS'") 

    def get_wave_shape(self): 
        ''' 
        Read current waveform shape 
        ''' 
        get_var = self.comm('FUNC?')[:-1] 
        return(get_var) 

    def set_volt_unit(self,unit='VPP'): 
        ''' 
        Choose output voltage units. VPP, VRMS or DBM 
        ''' 
        if 'VR' in unit.upper(): 
            self.comm('VOLT:UNIT VRMS') 
        elif 'VP' in unit.upper(): 
            self.comm('VOLT:UNIT VPP') 
        elif 'D' in unit.upper(): 
            self.comm('VOLT:UNIT DBM') 
        else: 
            print("Choose correct unit: 'VPP','VRMS' or 'DBM'") 

    def get_volt_unit(self): 
        return(self.comm('VOLT:UNIT?')[:-1])         


    def set_volt_ampl_offs(self,Vpp=2,Voffset=1): 
        ''' 
        Sets output voltage in terms of amplitude and Voffset 
        ''' 
        self.set_volt_unit('VPP') 
        load = float(self.comm('OUTP:LOAD?')) 
        if load == 50: 
            Vpp = min(10,Vpp) 
        else: 
            Vpp = min(20,Vpp) 
        self.comm('VOLT {}'.format(Vpp)) 
        self.comm('VOLT:OFFSET {}'.format(Voffset)) 


    def set_volt_vh_vl(self,v_high=3.3,v_low=0): 
        ''' 
        Sets output votlage in terms of VHigh and VLow 
        ''' 
        self.set_volt_unit('VPP') 
        self.comm('VOLT:HIGH {}'.format(v_high)) 
        self.comm('VOLT:LOW {}'.format(v_low)) 

    def get_volt_vh_vl(self): 
        ''' 
        Returns Vhigh and Vlow 
        ''' 
        get_var1 = float(self.comm('VOLT:HIGH?')) 
        get_var2 = float(self.comm('VOLT:LOW?')) 
        return(get_var1,get_var2) 

    def set_volt_dBm(self,pow_dBm=6): 
        ''' 
        Set output in dBm 
        ''' 
        self.set_volt_unit('DBM') 
        self.comm('VOLT {}'.format(pow_dBm)) 

    def get_volt_ampl_offs(self,read_voffset = 'NO'): 
        ''' 
        Read amplitude and if read_offset = Y, read V_offset 
        ''' 
        if self.get_volt_unit == 'DBM': 
            print('Voltage unit is in dBm') 
            return(float(self.comm('VOLT?'))) 
        else: 
            get_var1 = float(self.comm('VOLT?')) 
            get_var2 = float(self.comm('VOLT:OFFS?')) 
            print() 
        if read_voffset.upper() in 'NO': 
            print('Returns Vpp only. Pass Y to get Voffset') 
            print('Units= ',self.get_volt_unit()) 
            return(get_var1) 
        else: 
            print('Units= ',self.get_volt_unit()) 
            return(get_var1,get_var2) 


    def set_duty_cycle(self,dc=50): 
        ''' 
        Set duty cycle for a sqaure wave 
        ''' 
        if self.get_wave_shape() in 'SQUARE':         
            self.comm('FUNC:SQU:DCYC {}'.format(dc)) 
        else: 
            print('Current waveform is not Square. Set Squ and try again') 

    def get_duty_cycle(self): 
        ''' 
        Get duty cycle of a square waveform 
        ''' 
        if self.get_wave_shape() in 'SQUARE':         
            get_var = float(self.comm('FUNC:SQU:DCYC?')) 
            return(get_var) 
        else: 
            print('Current waveform is not Square. Set Squ and try again') 


    def set_out_state(self,state='ON'): 
        ''' 
        Switch output ON or OFF 
        ''' 
        self.comm('OUTP {}'.format(state)) 

    def get_out_state(self): 
        ''' 
        Returns current output state 
        ''' 
        get_var = float(self.comm('OUTP?')) 
        return(get_var) 

    def set_out_load(self,load='INF'): 
        ''' 
        Choose output impedance; 50, INF 
        ''' 
        if type(load) == 'str': 
            l = 'INF' 
        else: 
            l = float(load) 
            self.comm('OUTP:LOAD {}'.format(l)) 

    def get_out_load(self): 
        get_var = self.comm('OUTP:LOAD?')[:-1] 
        if type(get_var) == 'str': 
            return('INF') 
        else: 
            return(float(get_var)) 


