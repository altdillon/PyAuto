from cInst_oscilloscope import cInst_oscilloscope
import time

class cInst_MSO58LP(cInst_oscilloscope):
    '''
    TBD
    '''

    def set_pna(self, channel):
        '''
        Sets the scope to PNA mode
        '''
        self.comm(f'SV:CH{channel}:SELect:RF_PHASe ON')
























    def set_auto_scale(self, plot):
        """Performs front panel equivalent of AUTOSET"""
        self.comm(f"DISplay:PLOTView{plot}:AUTOScale")

    def set_persistence(self, state):
        '''
        Sets the state of persistence (resets if already on)
        state : boolean as to whther or not persistence is on
        '''
        if state:
            self.comm('DISplay:PERSistence AUTO')
        else:
            self.comm('DISplay:PERSistence OFF')

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Horizontal Methods           '''
    ''''''''''''''''''''''''''''''''''''''''''''''''

    def set_sampling_rate(self, rate):
        """
        Set the sampling rate of the scope. Based on the time axis duration, the value set may be adjusted automatically by the scope
        rate : sampling rate in samples/second
        """
        self.comm(f"HOR:SAMPLER {rate}")

    def get_sampling_rate(self):
        """
        Returns set sampling rate
        """
        return float(self.comm("HOR:SAMPLER?"))

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Horizontal Methods           '''
    ''''''''''''''''''''''''''''''''''''''''''''''''


    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Channel Methods              '''
    ''''''''''''''''''''''''''''''''''''''''''''''''

    def set_vertical_scale(self, channel, scale, math = False, waveview = 1):
        '''
        Sets the vertical scale of the given channel in V/div
        channel : integer of the channel
        scale : Veritcal scale in V/div
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            self.comm(f"DISplay:WAVEView{waveview}:MATH:MATH{channel}:VERTical:SCA {scale}")
        else:
            self.comm(f'CH{channel}:SCA {scale}')

    def get_vertical_scale(self, channel, math = False):
        '''
        Returns the vertical scale in V/div of the given channel
        channel: integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            return float(self.comm(f"DISplay:WAVEView{waveview}:MATH:MATH{channel}:VERTical:SCA?"))
        else:
            return float(self.comm(f"CH{channel}:SCA?"))

    def set_vertical_position(self, channel, position, math = False, waveview = 1):
        '''
        Sets the vertical position for a given channel in V
        channel : integer of the channel
        position : Veritcal position in V
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            self.comm(f"DISplay:WAVEView{waveview}:MATH:MATH{channel}:VERTical:POS {position}")
        else:
            self.comm(f"CH{channel}:POS {position}")

    def get_vertical_position(self, channel, math = False):
        '''
        Returns the vertical position for a given channel in V
        channel : integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            return float(self.comm(f"DISplay:WAVEView{waveview}:MATH:MATH{channel}:VERTical:POS"))
        else:
            return float(self.comm(f"CH{channel}:POS?"))

    def set_channel_state(self, channel, state, math = False):
        '''
        Sets the display state of the specified channel
        channel : integer of the channel
        state : Boolean or 1/0 integer describing the display state of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            if state:
                self.comm(f"DISplay:GLObal:MATH{channel}:STATE ON")
            else:
                self.comm(f"DISplay:GLObal:MATH{channel}:STATE OFF")
        else:
            if state:
                self.comm(f"DISplay:GLObal:CH{channel}:STATE ON")
            else:
                self.comm(f"DISplay:GLObal:CH{channel}:STATE OFF")

    def get_channel_state(self, channel, math = False):
        '''
        Returns the display state of the specified channel as 1 or 0
        channel : integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            return int(self.comm(f"DISplay:GLObal:MATH{channel}:STATE?"))
        else:
            return int(self.comm(f"DISplay:GLObal:CH{channel}:STATE?"))

    def set_channel_deskew(self, channel, deskew):
        '''
        Sets the deskew value of the given channel
        channel : integer of the channel
        deskew :  time value (in seconds) to shift the channel between -75ns and 75ns
        '''
        if deskew < -125e-9 or deskew > 125e-9:
            raise ValueError("Deskew must be bewteen +/- 75ns represented in seconds")
        self.comm(f"CH{channel}:DESKEW {deskew}")

    def set_math(self, channel1, channel2, operation, channel = None):
        """
        Sets up a math operation ({channel1} {operation} {channel2})
        channel1 : integer of first channel in equation
        channel2 : integer of second channel in equation
        operation : '+', '-', '*', '/'
        channel : integer of math channel to set up (if unspecified, adds a new math signal)
        """
        if channel == None:
            channel = 1
            while True:
                if not self.get_channel_state(i, True):
                    break
                channel += 1
        
        self.comm(f'MATH:ADDNEW "MATH{channel}"')

        self.comm(f'MATH:MATH{channel}:TYPe ADVANCED')

        self.comm(f"MATH{channel}:DEFINE CH{channel1}{operation}CH{channel2}")

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Channel Methods              '''
    ''''''''''''''''''''''''''''''''''''''''''''''''


    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Measurement Methods          '''
    ''''''''''''''''''''''''''''''''''''''''''''''''

    def set_measurement(self, mtype, channel, math = False, measurement_number = None, channel2 = None, math2 = None, edge1 = 1, edge2 = 1, direction = 1):
        """
        Sets up measurement
        ------ mtype ------
        'amplitude'         ->  Amplitude of the signal. High - low
        'high'              ->  High point of waveform; excluding overshoot
        'low'               ->  Low point of waveform; excluding undershoot
        'max'               ->  Maximum point including overshoot
        'min'               ->  Mininum point including undershoot
        'mean'              ->  Mean point of the waveform (usually vcm)
        'pk2pk'             ->  Peak to peak value, usually > amplitude
        'under'             ->  Undershoot = low - min percentage
        'over'              ->  Overshoot = max - high percentage
        'rise'              ->  Rise time(default 10-90 %)
        'fall'              ->  Fall time(default 10-90 %)
        'pduty'             ->  Duty cycle of high duration
        'nduty'             ->  Duty cycle of low duration  
        'frequency'         ->  Frequency
        'delay'             ->  Delay between two channels

        channel : integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        measurement_number : integer between 1 and 8
        edge1 : used for delay measurement, boolean or 0/1 for rise (1) or fall (0) edge
        edge2 : used for delay measurement, boolean or 0/1 for rise (1) or fall (0) edge
        direction : used for delay measurement, boolean or 0/1 for forward (1) or backwards (0)
                 
        """
        if measurement_number == None:
            self.comm('MEASU:ADDMEAS')
            measurement_number = len(self.comm('MEASU:LIST?').split(,))

        if math:
            channel_type = 'MATH'
        else:
            channel_type = 'CH'

        if mtype.lower() in 'amplitude':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP AMPL')
        elif mtype.lower() in 'rise':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP RISE')
        elif mtype.lower() in 'fall':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP FALL')
        elif mtype.lower() in 'pk2pk':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP PK2PK')
        elif mtype.lower() in 'frequency':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP FREQ')
        elif mtype.lower() in 'pduty':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP PDUTY')
        elif mtype.lower() in 'nduty':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP NDUTY')
        elif mtype.lower() in 'high':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP HIGH')
        elif mtype.lower() in 'low':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP LOW')
        elif mtype.lower() in 'max':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP MAX')
        elif mtype.lower() in 'min':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP MINI')
        elif mtype.lower() in 'mean':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP MEAN')
        elif mtype.lower() in 'over':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP POV')
        elif mtype.lower() in 'under':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP NOV')
        elif mtype.lower() in 'delay':
            if math2:
                channel_type2 = 'MATH'
            else:
                channel_type2 = 'CH'

            if direction:
                direction  = "FORW"
            else:
                direction  = "BACKW"

            if edge1:
                edge1 = 'RISE'
            else:
                edge1 = 'FALL'

            if edge2:
                edge2 = 'RISE'
            else:
                edge2 = 'FALL'

            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; SOU2 {channel_type2}{channel2};TYP DELAY')
            self.comm(f"MEASU:MEAS{measurement_number}:DEL:EDGE1 {edge1}")
            self.comm(f"MEASU:MEAS{measurement_number}:DEL:EDGE2 {edge2}")
            self.comm(f"MEASU:MEAS{measurement_number}:DEL:DIRE {direction}")
        else:
            raise ValueError("mtype mus be one of the following:  ['amplitude', 'high', 'low', 'max', 'min', 'mean', 'pk2pk', 'under', 'over', 'rise', 'fall', 'pduty', 'nduty', 'frequency', 'delay']")

    def get_measurement(self, measurement_number):
        '''
        Returns a dictionary of the measurement parameters [type, channel, math, (channel2, math2, edge1, edge2, direction)]
        measurement_number : integer of the measurement
        '''
        if f'MEAS{measurement_number}' not in self.comm('MEASU:LIST?'):
            raise ValueError('The measurement for this measurement_number is not set up')

        ret = {}

        mtype = self.comm(f'MEASU:MEAS{measurement_number}:TYP?')
        if mtype.lower() in 'amplitude':
            ret['type'] = 'amplitude'
        elif mtype.lower() in 'rise':
            ret['type'] = 'rise'
        elif mtype.lower() in 'fall':
            ret['type'] = 'fall'
        elif mtype.lower() in 'pk2pk':
            ret['type'] = 'pk2pk'
        elif mtype.lower() in 'frequency':
            ret['type'] = 'frequency'
        elif mtype.lower() in 'pduty':
            ret['type'] = 'pduty'
        elif mtype.lower() in 'nduty':
            ret['type'] = 'nduty'
        elif mtype.lower() in 'high':
            ret['type'] = 'high'
        elif mtype.lower() in 'low':
            ret['type'] = 'low'
        elif mtype.lower() in 'max':
            ret['type'] = 'max'
        elif mtype.lower() in 'mini':
            ret['type'] = 'min'
        elif mtype.lower() in 'mean':
            ret['type'] = 'mean'
        elif mtype.lower() in 'pov':
            ret['type'] = 'over'
        elif mtype.lower() in 'nov':
            ret['type'] = 'under'
        elif mtype.lower() in 'delay':
            ret['type'] = 'delay'
        else:
            ret['type'] = 'unknown'


            source = self.comm(f'MEASU:MEAS{measurement_number}:SOU2?')
            ret['math2'] = 'MATH' in source.upper():
            ret['channel2'] = int(source[-2:-1])
            edge1 = self.comm(f"MEASU:MEAS{measurement_number}:DEL:EDGE1?")[:-1]
            if edge1.lower() in 'rise':
                ret['edge1'] = 1
            elif edge1.lower() in 'fall':
                ret['edge1'] = 0
            else:
                ret['edge1'] = 'unknown'
            edge2 = self.comm(f"MEASU:MEAS{measurement_number}:DEL:EDGE2?")[:-1]
            if edge2.lower() in 'rise':
                ret['edge2'] = 1
            elif edge2.lower() in 'fall':
                ret['edge2'] = 0
            else:
                ret['edge2'] = 'unknown'
            direction = self.comm(f"MEASU:MEAS{measurement_number}:DEL:DIRE?")[:-1]
            if direction.lower() in 'forward':
                ret['direction'] = 1
            elif direction.lower() in 'backward':
                ret['direction'] = 0
            else:
                ret['direction'] = 'unknown'
            

        source = self.comm(f'MEASU:MEAS{measurement_number}:SOU1?')
        ret['math'] = 'MATH' in source.upper():
        ret['channel'] = int(source[-2:-1])

        return ret

    def meas_measurement(self, measurement_number):
        '''
        Returns the last captured value of the measurement (actually the mean for this scope)
        measurement_number : integer of measurement
        '''
        return float(self.comm(f'MEASUrement:MEAS{measurement_number}:RESUlts:CURRentacq:MEAN?'))

    def meas_mean_measurement(self,measurement_number):
        '''
        Returns the mean of the measurement
        measurement_number : integer of measurement
        '''
        return float(self.comm(f'MEASUrement:MEAS{measurement_number}:RESUlts:CURRentacq:MEAN?'))

    def meas_max_measurement(self,measurement_number):
        """
        Returns the max of the measurement
        measurement_number : integer of measurement
        """
        return float(self.comm(f"MEASUrement:MEAS{measurement_number}:RESUlts:CURRentacq:MAX?"))

    def meas_min_measurement(self,measurement_number):
        """
        Returns the min of the measurement
        measurement_number : integer of measurement
        """
        return float(self.comm(f"MEASUrement:MEAS{measurement_number}:RESUlts:CURRentacq:MIN?"))   

    def set_measurement_reference(self, measurement_number, reference_type, edge, threshold, level):
        '''
        Sets the measurement reference position
        measurement_number : integer of measurement
        reference_type : 'percent' or 'absolute'
        edge : 'rise' or 'fall'
        threshold : 'high', 'mid', or 'low'
        level : a percentage if reference type is 'percent' or a voltage if reference type is 'absolute'
        '''
        if reference_type.upper() in 'PERCENT':
            self.comm(f'MEASU:MEAS{measurement_number}:REFLevels1:METHod PERcent')
            self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:PERCENT:{edge.upper()}{threshold.upper()} {level}")
            
        elif reference_type.upper() in 'ABSOLUTE':
            self.comm(f'MEASU:MEAS{measurement_number}:REFLevels1:METHod ABSolute')
            self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:ABS:{edge.upper()}{threshold.upper()} {level}")

        else:
            raise ValueError('reference_type must be either "percent" or "absolute"')

    def get_measurement_reference(self, measurement_number):
        '''
        Returns a dictionary of the measurement reference postion parameters [reference_type, threshold, level]
        measurement_number : integer of the measurement
        '''
        ret = {}
        reference_type = self.comm(f'MEASU:MEAS{measurement_number}:REFLevel:METHod?')
        if reference_type.lower() in 'percent':
            ret['reference_type'] = 'percent'
            ret['rise_high'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:PERCENT:RISEHIGH?"))
            ret['rise_mid'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:PERCENT:RISEMID?"))
            ret['rise_low'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:PERCENT:RISELOW?"))    
            ret['rise_high'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:PERCENT:FALLHIGH?"))
            ret['rise_mid'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:PERCENT:FALLMID?"))
            ret['rise_low'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:PERCENT:FALLLOW?"))  
        elif reference_type.lower() in 'absolute':
            ret['reference_type'] = 'absolute'
            ret['rise_high'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:ABSOLUTE:RISEHIGH?"))
            ret['rise_mid'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:ABSOLUTE:RISEMID?"))
            ret['rise_low'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:ABSOLUTE:RISELOW?"))  
            ret['rise_high'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:ABSOLUTE:FALLHIGH?"))
            ret['rise_mid'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:ABSOLUTE:FALLMID?"))
            ret['rise_low'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevels1:ABSOLUTE:FALLLOW?"))  
        else:
            ret['reference_type'] = 'unknown'
            ret['rise_high'] = 'unknown'
            ret['rise_mid'] = 'unknown'
            ret['rise_low'] = 'unknown'
            ret['fall_high'] = 'unknown'
            ret['fall_mid'] = 'unknown'
            ret['fall_low'] = 'unknown'
        
    def reset_measurement_statistics(self):
        '''
        Resets the measurement stats
        '''
        self.comm("MEASUrement:STATIstics:CYCLEMode 0")
        self.comm("MEASUrement:STATIstics:CYCLEMode 1")

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Measurement Methods          '''
    ''''''''''''''''''''''''''''''''''''''''''''''''


    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Trigger Methods              '''
    ''''''''''''''''''''''''''''''''''''''''''''''''

    def set_trigger_level(self, trigger, level, channel, math = False):
        """
        Returns trigger level in volts
        trigger : 'a' or 'b'
        level : voltage value (V) or "center"
        """ 
        if math:
            channel_type = 'MATH'
        else:
            channel_type = 'CH'
        self.comm(f"TRIG:{trigger.upper()}:LEV:{channel_type}{channel} {level}")
    
    def set_trigger_edge(self, trigger, edge):
        """
        Returns trigger edge direction
        trigger : 'a' or 'b'
        edge : 'rise', 'fall', or 'either'
        """ 
        if edge.upper() in "RISE":
            self.comm(f"TRIG:{trigger.upper()}:EDGE:SLOPE RISE")
        elif edge.upper() in "FALL":
            self.comm(f"TRIG:{trigger.upper()}:EDGE:SLOPE FALL")
        else:
            self.comm(f"TRIG:{trigger.upper()}:EDGE:SLOPE EITHER")

    def get_trigger_level(self, trigger):
        """
        Returns trigger level in volts
        trigger : 'a' or 'b'
        """ 
        return float(self.comm(f"TRIG:{trigger.upper()}:LEV:{channel_type}{channel}?"))
    
    def get_trigger_edge(self, trigger):
        """
        Returns trigger edge direction
        trigger : 'a' or 'b'
        """ 
        return self.comm(f"TRIG:{trigger.upper()}:EDGE:SLOPE?")[:-1]

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Trigger Methods              '''
    ''''''''''''''''''''''''''''''''''''''''''''''''   

   
    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Trace/Plot Methods           '''
    ''''''''''''''''''''''''''''''''''''''''''''''''   

    def get_plot(self, filename, invert = False):
        '''
        Gets plot from scope and saves it to the filename (full path) as a png passed to the function
        '''
        if invert:
            self.comm("SAV:IMAG:COMP INVE")
        else:
            self.comm("SAV:IMAG:COMP NORM")

        self.comm('SAV:IMAG "C:/temp.png"')
        time.sleep(3)
        self.comm('FILES:READF "C:/temp.png"')
        time.sleep(1)
        timeout = self.inst.timeout
        self.inst.timeout = 5000
        try:
            raw = self.inst.read_raw()
        except:
            #Timed out. Trying with longer Timeout
            self.comm("CLS")
            self.inst.timeout = 10000
            try:
                raw = self.inst.read_raw()
            except:
                print("Failed to aquire data from device. Saved this to file and continued test")
                raw = "Failed to aquire data from device. Saved this to file and continued test"

        self.inst.timeout = timeout

        try:
            '''If this works then the scope returned data'''
            with open(filename,'wb') as fp:
                fp.write(raw)
        except:
            '''Otherwise, the string from above needs to be written'''
            with open(filename + '.txt','w') as fp:
                fp.write(raw)

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Trace/Plot Methods           '''
    ''''''''''''''''''''''''''''''''''''''''''''''''   

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Run/Acquisition Methods      '''
    '''''''''''''''''''''''''''''''''''''''''''''''' 
    
    #no changes were needed to these functions

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Run/Acquisition Methods      '''
    '''''''''''''''''''''''''''''''''''''''''''''''' 
