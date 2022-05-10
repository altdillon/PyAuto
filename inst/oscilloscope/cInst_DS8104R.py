from cInst_oscilloscope import cInst_oscilloscope

class cInst_DS8104R(cInst_oscilloscope):
    '''
    TBD
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.dict_measurements = {}
        self.run_mode = 'run'
        self.run_state = 1

    def set_auto_scale(self):
        """Performs front panel equivalent of AUTOSET"""
        self.comm("SYST:AUT ON")
        self.comm("AUT")

    def set_persistence(self, state):
        '''
        Sets the state of persistence (resets if already on)
        state : boolean as to whther or not persistence is on
        '''
        if state:
            self.comm('DISPlay:GRADing:TIME INF')
            self.comm('DISPlay:CLEar')
        else:
            self.comm('DISPlay:GRADing:TIME MIN')

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Horizontal Methods           '''
    ''''''''''''''''''''''''''''''''''''''''''''''''

    def set_time_scale(self, time_scale):
        '''
        sets horizontal scale (seconds/division)
        '''
        self.comm(f'TIM:SCAL {time_scale}')

    def get_time_scale(self):
        """
        Returns the time base(second per division)
        """
        return float(self.comm("TIM:SCAL?"))

    def set_time_delay(self, delay):
        '''
        Sets the horizontal delay in seconds
        '''
        self.comm(f'TIM:DEL:OFFS {delay}')

    def get_time_delay(self):
        '''
        Returns the horizontal delay in seconds
        '''
        return float(self.comm(f'TIM:DEL:OFFS?'))

    def set_sampling_rate(self, rate):
        """
        Set the sampling rate of the scope. Based on the time axis duration, the value set may be adjusted automatically by the scope
        rate : sampling rate in samples/second
        """
        #get waveform length
        waveform_length = self.get_time_scale()*10
        #set mdepth = srate*waveform_length
        self.comm(f"ACQ:MDEP {rate*waveform_length}")

    def get_sampling_rate(self):
        """
        Returns set sampling rate
        """
        return float(self.comm("ACQ:SRAT?"))

    def set_record_length(self, record_length):
        """
        Sets the number of points that can be acquired per waveform with current time base and sampling rate setting
        record_length = numeric value
        """
        self.comm(f"ACQ:MDEP {record_length}")

    def get_record_length(self):
        """
        Returns the current record length
        """
        return float(self.comm(f"ACQ:MDEP?"))

    def set_horizontal_mode(self, mode):
        """
        Sets the mode to determine correlation between sampling rate, time base and record length
        mode = 'Auto'       Auto mode attempts to keep record length constant as you change the time per division setting. Record length is read only
             = 'Constant'   Constant mode attempts to keep sample rate constant as you change the time per division setting. Record length is read only.
             = 'Manual'     Manual mode lets you change sample mode and record length. Time per division or Horizontal scale is read only
        """
        pass

    def get_horizontal_mode(self):
        """
        Return the horizontal mode. This mode determine correlation between sampling rate, time base and record length 
        """
        return 'Constant'


    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Horizontal Methods           '''
    ''''''''''''''''''''''''''''''''''''''''''''''''


    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Channel Methods              '''
    ''''''''''''''''''''''''''''''''''''''''''''''''

    def set_vertical_scale(self, channel, scale, math = False):
        '''
        Sets the vertical scale of the given channel in V/div
        channel : integer of the channel
        scale : Veritcal scale in V/div
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            self.comm(f"MATH{channel}:SCAL {scale}")
        else:
            self.comm('CHAN:VERN ON')
            self.comm(f'CHAN{channel}:SCAL {scale}')

    def get_vertical_scale(self, channel, math = False):
        '''
        Returns the vertical scale in V/div of the given channel
        channel: integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            return float(self.comm(f"MATH{channel}:SCAL?"))
        else:
            return float(self.comm(f"CHAN{channel}:SCAL?"))

    def set_vertical_position(self, channel, position, math = False):
        '''
        Sets the vertical position for a given channel in V
        channel : integer of the channel
        position : Veritcal position in V
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            self.comm(f"MATH{channel}:OFFS {position}")
        else:
            self.comm(f"CHAN{channel}:OFFS {position}")

    def get_vertical_position(self, channel, math = False):
        '''
        Returns the vertical position for a given channel in V
        channel : integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            return float(self.comm(f"MATH{channel}:OFFS?"))
        else:
            return float(self.comm(f"CHAN{channel}:OFFS?"))

    def set_termination(self, channel, termination):
        '''
        Sets the termination of the channel
        channel : integer of the channel
        termination : Either 50 or 1e6
        '''
        if termination not in [50, 1e6]:
            raise ValueError('Unknown Termination Value. Set to either 50 or 1e6')
        if termination == 50:
            self.comm(f"CHAN{channel}:IMP FIFT")
        else:
            self.comm(f"CHAN{channel}:IMP OMEG")

    def get_termination(self, channel):
        '''
        Returns the termination of the channel
        channel : integer of the channel
        '''
        ter = self.comm(f"CHAN{channel}:IMP?")
        if 'FIFT' in ter:
            return 50
        else:
            return 1e6

    def set_channel_state(self, channel, state, math = False):
        '''
        Sets the display state of the specified channel
        channel : integer of the channel
        state : Boolean or 1/0 integer describing the display state of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            if state:
                self.comm(f"MATH{channel}:DISP ON")
            else:
                self.comm(f"MATH{channel}:DISP OFF")
        else:
            if state:
                self.comm(f"CHAN{channel}:DISP ON")
            else:
                self.comm(f"CHAN{channel}:DISP OFF")

    def get_channel_state(self, channel, math = False):
        '''
        Returns the display state of the specified channel as 1 or 0
        channel : integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            return int(self.comm(f"MATH{channel}:DISP?"))
        else:
            return int(self.comm(f"CHAN{channel}:DISP?"))

    def set_channel_deskew(self, channel, deskew):
        '''
        Sets the deskew value of the given channel
        channel : integer of the channel
        deskew :  time value (in seconds) to shift the channel between -75ns and 75ns
        '''
        if deskew < -100e-9 or deskew > 100e-9:
            raise ValueError("Deskew must be bewteen +/- 100ns represented in seconds")
        self.comm(f"CHAN{channel}:PROB:DEL {deskew}")
        
    def get_channel_deskew(self, channel):
        '''
        Returns the deskew value of the given channel in seconds
        channel : integer of the channel
        '''
        return float(self.comm(f"CHAN{channel}:PROB:DEL?"))

    def set_math(self, channel1, channel2, operation, channel = None):
        """
        Sets up a math operation ({channel1} {operation} {channel2})
        channel1 : integer of first channel in equation
        channel2 : integer of second channel in equation
        operation : '+' or '-'
        channel : integer of math channel to set up (if unspecified, adds a new math signal)
        """
        if channel == None:
            for i in range(1,4):
                if self.get_channel_state(i, True):
                    channel = i + 1

        if operation == '+':
            self.comm(f"MATH{channel}:OPER ADD")
        elif operation == '-':
            self.comm(f"MATH{channel}:OPER SUBT")
        else:
            raise ValueError('Unknown operator. Use either "+" or "-".')

        self.comm(f"MATH{channel}:SOUR1 CHAN{channel1}")
        self.comm(f"MATH{channel}:SOUR2 CHAN{channel2}")
        self.set_channel_state(channel, 1, True)

    def get_math(self, channel):
        '''
        Returns the string representation of the math equation
        '''
        operation = self.comm(f"MATH{channel}:OPER?")
        if 'ADD' in operation:
            operation = '+'
        elif 'SUBT' in operation:
            operation = '-'
        else:
            operation = '?'

        channel1 = self.comm(f"MATH{channel}:SOUR1?")[:-1]
        channel2 = self.comm(f"MATH{channel}:SOUR2?")[:-1]

        return channel1 + operation + channel2

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
            measurement_number = (len(self.dict_measurements) + 1)

        #[type, channel, math, (channel2, math2, edge1, edge2, direction)]
        self.dict_measurements[measurement_number] = {  'type': mtype,
                                                        'channel': channel,
                                                        'math': math,
                                                        'channel2': channel2,
                                                        'math2': math2,
                                                        'edge1': edge1,
                                                        'edge2': edge2,
                                                        'direction': direction}

        if math:
            channel_type = 'MATH'
        else:
            channel_type = 'CHAN'

        if mtype.lower() in 'amplitude':
            self.comm(f'MEAS:ITEM VAMP,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM VAMP,{channel_type}{channel}')
        elif mtype.lower() in 'rise':
            self.comm(f'MEAS:ITEM RTIM,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM RTIM,{channel_type}{channel}')
        elif mtype.lower() in 'fall':
            self.comm(f'MEAS:ITEM FTIM,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM FTIM,{channel_type}{channel}')
        elif mtype.lower() in 'pk2pk':
            self.comm(f'MEAS:ITEM VPP,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM VPP,{channel_type}{channel}')
        elif mtype.lower() in 'frequency':
            self.comm(f'MEAS:ITEM FREQ,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM FREQ,{channel_type}{channel}')
        elif mtype.lower() in 'pduty':
            self.comm(f'MEAS:ITEM PDUTY,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM PDUTY,{channel_type}{channel}')
        elif mtype.lower() in 'nduty':
            self.comm(f'MEAS:ITEM NDUTY,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM NDUTY,{channel_type}{channel}')
        elif mtype.lower() in 'high':
            self.comm(f'MEAS:ITEM VUPP,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM VUPP,{channel_type}{channel}')
        elif mtype.lower() in 'low':
            self.comm(f'MEAS:ITEM VLOW,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM VLOW,{channel_type}{channel}')
        elif mtype.lower() in 'max':
            self.comm(f'MEAS:ITEM VMAX,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM VMAX,{channel_type}{channel}')
        elif mtype.lower() in 'min':
            self.comm(f'MEAS:ITEM VMIN,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM VMIN,{channel_type}{channel}')
        elif mtype.lower() in 'mean':
            self.comm(f'MEAS:ITEM VAVG,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM VAVG,{channel_type}{channel}')
        elif mtype.lower() in 'over':
            self.comm(f'MEAS:ITEM OVER,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM OVER,{channel_type}{channel}')
        elif mtype.lower() in 'under':
            self.comm(f'MEAS:ITEM PRES,{channel_type}{channel}')
            self.comm(f'MEAS:STAT:ITEM PRES,{channel_type}{channel}')
        elif mtype.lower() in 'delay':
            if math2:
                channel_type2 = 'MATH'
            else:
                channel_type2 = 'CHAN'

            if edge1:
                edge1 = 'R'
            else:
                edge1 = 'F'

            if edge2:
                edge2 = 'R'
            else:
                edge2 = 'F'

            self.comm(f'MEAS:ITEM {edge1}{edge2}D,{channel_type}{channel},{channel_type2}{channel2}')
            self.comm(f'MEAS:STAT:ITEM {edge1}{edge2}D,{channel_type}{channel},{channel_type2}{channel2}')
        else:
            raise ValueError("mtype must be one of the following:  ['amplitude', 'high', 'low', 'max', 'min', 'mean', 'pk2pk', 'under', 'over', 'rise', 'fall', 'pduty', 'nduty', 'frequency', 'delay']")

    def get_measurement(self, measurement_number):
        '''
        Returns a dictionary of the measurement parameters [type, channel, math, (channel2, math2, edge1, edge2, direction)]
        measurement_number : integer of the measurement
        '''
        return self.dict_measurements[measurement_number]

    def meas_measurement(self, measurement_number):
        '''
        Returns the last captured value of the measurement
        measurement_number : integer of measurement
        '''
        if self.dict_measurements[measurement_number]['channel2'] == None:
            return float(f"MEAS:ITEM? {self.dict_measurements[measurement_number]['type']},{self.dict_measurements[measurement_number]['channel']}")
        else:
            return float(f"MEAS:ITEM? {self.dict_measurements[measurement_number]['type']},{self.dict_measurements[measurement_number]['channel']},{self.dict_measurements[measurement_number]['channel2']}")

    def meas_mean_measurement(self,measurement_number):
        '''
        Returns the mean of the measurement
        measurement_number : integer of measurement
        '''
        if self.dict_measurements[measurement_number]['channel2'] == None:
            return float(f"MEAS:STAT:ITEM? AVER,{self.dict_measurements[measurement_number]['type']},{self.dict_measurements[measurement_number]['channel']}")
        else:
            return float(f"MEAS:STAT:ITEM? AVER,{self.dict_measurements[measurement_number]['type']},{self.dict_measurements[measurement_number]['channel']},{self.dict_measurements[measurement_number]['channel2']}")

    def meas_max_measurement(self,measurement_number):
        """
        Returns the max of the measurement
        measurement_number : integer of measurement
        """
        if self.dict_measurements[measurement_number]['channel2'] == None:
            return float(f"MEAS:STAT:ITEM? MAX,{self.dict_measurements[measurement_number]['type']},{self.dict_measurements[measurement_number]['channel']}")
        else:
            return float(f"MEAS:STAT:ITEM? MAX,{self.dict_measurements[measurement_number]['type']},{self.dict_measurements[measurement_number]['channel']},{self.dict_measurements[measurement_number]['channel2']}")

    def meas_min_measurement(self,measurement_number):
        """
        Returns the min of the measurement
        measurement_number : integer of measurement
        """
        if self.dict_measurements[measurement_number]['channel2'] == None:
            return float(f"MEAS:STAT:ITEM? MIN,{self.dict_measurements[measurement_number]['type']},{self.dict_measurements[measurement_number]['channel']}")
        else:
            return float(f"MEAS:STAT:ITEM? MIN,{self.dict_measurements[measurement_number]['type']},{self.dict_measurements[measurement_number]['channel']},{self.dict_measurements[measurement_number]['channel2']}")

    def set_measurement_reference(self, measurement_number, reference_type, threshold, level):
        '''
        Sets the measurement reference position
        measurement_number : integer of measurement
        reference_type : 'percent' or 'absolute'
        threshold : 'high', 'mid', or 'low'
        level : a percentage if reference type is 'percent' or a voltage if reference type is 'absolute'
        '''
        if reference_type.upper() in 'PERCENT':
            if threshold.upper() in 'HIGH':
                self.comm(f"MEAS:SET:MAX {level}")
            elif threshold.upper() in 'MID':
                self.comm(f"MEAS:SET:MID {level}")
            elif threshold.upper() in 'LOW':
                self.comm(f"MEAS:SET:MIN {level}")
            else:
                raise ValueError('threshold must be "high", "mid", or "low"')
        else:
            raise ValueError('Only supports "percent" reference type')

    def get_measurement_reference(self, measurement_number):
        '''
        Returns a dictionary of the measurement reference postion parameters [reference_type, threshold, level]
        measurement_number : integer of the measurement
        '''
        ret = {}
        ret['reference_type'] = 'percent'
        ret['level_high'] = float(self.comm(f"MEAS:SET:MAX?"))
        ret['level_mid'] = float(self.comm(f"MEAS:SET:MID?"))
        ret['level_low'] = float(self.comm(f"MEAS:SET:MIN?"))    
        return ret

    def reset_measurement_statistics(self):
        '''
        Resets the measurement stats
        '''
        self.comm("MEAS:STAT:RES")

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Measurement Methods          '''
    ''''''''''''''''''''''''''''''''''''''''''''''''


    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Trigger Methods              '''
    ''''''''''''''''''''''''''''''''''''''''''''''''
        
    def set_trigger_source(self, trigger, channel, math):
        """
        Sets the trigger source
        trigger : 'a' or 'b'
        channel : integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        """
        if math:
            self.comm(f"TRIG:EDGE:SOUR MATH{channel}")
        else:
            self.comm(f"TRIG:EDGE:SOUR CHAN{channel}")

    def set_trigger_level(self, trigger, level):
        """
        Returns trigger level in volts
        trigger : 'a' or 'b'
        level : voltage value (V) or "center"
        """ 
        if level.lower() in 'center':
            self.comm(f"TRIG:EDGE:LEV 0")
        else:
            self.comm(f"TRIG:EDGE:LEV {level}")
    
    def set_trigger_edge(self, trigger, edge):
        """
        Returns trigger edge direction
        trigger : 'a' or 'b'
        edge : 'rise', 'fall', or 'either'
        """ 
        if edge.upper() in "RISE":
            self.comm(f"TRIG:EDGE:SLOPE POS")
        elif edge.upper() in "FALL":
            self.comm(f"TRIG:EDGE:SLOPE NEG")
        else:
            self.comm(f"TRIG:EDGE:SLOPE RFAL")

    def get_trigger_source(self, trigger):
        """
        Returns trigger source
        trigger : 'a' or 'b'
        """
        return self.comm(f"TRIG:EDGE:SOUR?")[:-1]

    def get_trigger_level(self, trigger):
        """
        Returns trigger level in volts
        trigger : 'a' or 'b'
        """ 
        return float(self.comm(f"TRIG:EDGE:LEV?"))
    
    def get_trigger_edge(self, trigger):
        """
        Returns trigger edge direction
        trigger : 'a' or 'b'
        """ 
        return self.comm(f"TRIG:EDGE:SLOPE?")[:-1]

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Trigger Methods              '''
    ''''''''''''''''''''''''''''''''''''''''''''''''   

   
    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Trace/Plot Methods           '''
    ''''''''''''''''''''''''''''''''''''''''''''''''   

    def get_plot(self, filename, invert = False):
        '''
        Gets the plot from scope and saves it to the filename (full path) as a png
        filename : full path of file to save image to (must end in .png)
        invert : boolean as to whether or not the color of the image is inverted
        '''
        self.comm("SAVE:IMAG:TYPE PNG")
        
        if invert:
            self.comm("SAVE:IMAG:INV ON")
        else:
            self.comm("SAVE:IMAG:INV OFF")
        
        self.comm("SAVE:IMAG 'C:\temp.png'")

        return "saved to device...can't seem to read from it..."

        '''

        self.comm("HARDCOPY START")
        time.sleep(3)
        self.comm("FILESYSTEM:READFILE 'C:\temp.png'")
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
            #image was transfered correctly
            with open(filename,'wb') as fp:
                fp.write(raw)
        except:
            #image was transfered incorrectly
            with open(filename + '.txt','w') as fp:
                fp.write(raw)
        '''

    def get_trace_data(self, channel, math = False):
        '''
        Returns the data points of the channel as a list of floats
        channel : integer of channel (0 = x data)
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            self.comm(f"WAV:SOU MATH{channel}")
        elif channel == 0:
            self.comm(f"WAV:SOU CHAN1")
        else:
            self.comm(f"WAV:SOU CHAN{channel}")

        self.comm(f"WAV:FORM ASC")

        xy_trace = [float(a) for a in self.comm("WAV:DATA?").split(",")[1:-1]]

        if channel == 0:
            xdata = []
            for x in range(float(self.comm('WAV:POIN?'))):
                xdata.appned(x/(self.get_sampling_rate()))
            return xdata
        else:
            return xy_trace

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Trace/Plot Methods           '''
    ''''''''''''''''''''''''''''''''''''''''''''''''   

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Run/Acquisition Methods      '''
    '''''''''''''''''''''''''''''''''''''''''''''''' 

    def set_run_mode(self, mode):
        """
        Sets the waveform acquisition run mode
        mode = 'run' or 'single'
        """
        if mode.upper() in "SINGLE":
            self.run_mode = 'single'
            self.comm(":SING")
        elif mode.upper() in "RUN":
            self.run_mode = 'run'
            self.comm(":RUN")
        else:
            raise ValueError('Unknown mode value. Please use either "single" or "run".') 

    def get_run_mode(self):
        """
        Gets the waveform acquisition run mode. Returns a string 'RUN' or 'SINGLE'
        """
        return self.run_mode

    def set_run_state(self, state):
        """
        Starts or stops the acquisition. Call this after setting set_run_mode('Single').
        state : boolean or 1/0
        """
        if state:
            self.run_state = 1
            if self.run_mode == 'run':
                self.comm(':RUN')
            else:
                self.comm(":SING")
        else:
            self.run_state = 0
            self.comm(":STOP")

    def get_run_state(self):
        """
        Gets the acquisition state
        """
        return self.run_state

    def set_acquisition_mode(self, mode):
        """
        Sets the acquisition type
        mode = sample, peakdet, hires, average, envelope
        """
        if mode.lower() in 'sample':
            self.comm('ACQ:TYPE NORM')
        elif mode.lower() in "peakdet":
            self.comm(f'ACQ:TYPE PEAK')
        elif mode.lower() in "hires":
            self.comm(f'ACQ:MOD HRES')
        elif mode.lower() in "average":
            self.comm(f'ACQ:MOD AVER')
        elif mode.lower() in "envelope":
            self.comm(f'ACQ:MOD NORM')
        else:
            raise ValueError('Unknown acquisition mode. Must be set to [sample, peakdet, hires, average, envelope]')

    def get_acquisition_mode(self):
        """
        Returns the acquisition mode as a string
        """
        mode = self.comm(f'ACQ:TYPE?')[:-1]
        if mode.lower() in "noraml":
            return 'sample'
        elif mode.lower() in "peakdet":
            return 'peakdet'
        elif mode.lower() in "hres":
            return 'hires'
        elif mode.lower() in "average":
            return 'average'
        elif mode.lower() in "envelope":
            return 'envelope'
        else:
            return 'unknown'
    
    def set_acquisition_average_count(self, count):
        """
        Sets the number of waveforms to be acquired in averaging mode. For this, the averaging mode must be selected with set_acquisition_mode('average').
        count : number of waveforms to average
        """
        self.comm(f"ACQ:AVER {count}")

    def get_acquisition_average_count(self):
        """
        Returns number of waveforms selected for average
        """
        return int(self.comm("ACQ:AVER?"))

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Run/Acquisition Methods      '''
    '''''''''''''''''''''''''''''''''''''''''''''''' 
