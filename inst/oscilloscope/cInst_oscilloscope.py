from cInst import cInst
import time

class cInst_oscilloscope(cInst):
    '''
    oscilloscope main class
    '''

    def set_auto_scale(self):
        """Performs front panel equivalent of AUTOSET"""
        self.comm("AUTOS EXEC")

    def set_persistence(self, state):
        '''
        Sets the state of persistence (resets if already on)
        state : boolean as to whther or not persistence is on
        '''
        if state:
            self.comm('DISplay:PERSistence ON')
            self.comm('DISplay:PERSistence:RESET')
        else:
            self.comm('DISplay:PERSistence OFF')

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Horizontal Methods           '''
    ''''''''''''''''''''''''''''''''''''''''''''''''

    def set_time_scale(self, time_scale):
        '''
        sets horizontal scale (seconds/division)
        '''
        self.comm(f'HORIZONTAL:SCA {time_scale}')

    def get_time_scale(self):
        """
        Returns the time base(second per division)
        """
        return float(self.comm("HOR:SCA?"))

    def set_time_delay(self, delay):
        '''
        Sets the horizontal delay in seconds
        '''
        self.comm(f'HOR:DEL:TIME {delay}')

    def get_time_delay(self):
        '''
        Returns the horizontal delay in seconds
        '''
        return float(self.comm(f'HOR:DEL:TIME?'))

    def set_sampling_rate(self, rate):
        """
        Set the sampling rate of the scope. Based on the time axis duration, the value set may be adjusted automatically by the scope
        rate : sampling rate in samples/second
        """
        self.comm(f"HOR:MAIN:SAMPLERATE {rate}")

    def get_sampling_rate(self):
        """
        Returns set sampling rate
        """
        return float(self.comm("HOR:MAIN:SAMPLER?"))

    def set_record_length(self, record_length):
        """
        Sets the number of points that can be acquired per waveform with current time base and sampling rate setting
        record_length = numeric value
        """
        self.comm(f"HOR:RECO {record_length}")

    def get_record_length(self):
        """
        Returns the current record length
        """
        return float(self.comm(f"HOR:RECO?"))

    def set_horizontal_mode(self, mode):
        """
        Sets the mode to determine correlation between sampling rate, time base and record length
        mode = 'Auto'       Auto mode attempts to keep record length constant as you change the time per division setting. Record length is read only
             = 'Constant'   Constant mode attempts to keep sample rate constant as you change the time per division setting. Record length is read only.
             = 'Manual'     Manual mode lets you change sample mode and record length. Time per division or Horizontal scale is read only
        """
        if mode.upper() in "CONSTANT":
            self.comm(f"HOR:MODE CONS")
        elif mode.upper() in "MANUAL":
            self.comm(f"HOR:MODE MAN")
        elif mode.upper() in "AUTO":
            self.comm(f"HOR:MODE AUTO")
        else:
            raise ValueError('Unknown mode value. Please use "AUTO", "CONSTANT", or "MANUAL".')

    def get_horizontal_mode(self):
        """
        Return the horizontal mode. This mode determine correlation between sampling rate, time base and record length 
        """
        return self.comm("HOR:MODE?")[:-1]


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
            self.comm(f"MATH{channel}:VERT:SCA {scale}")
        else:
            self.comm(f'CH{channel}:SCA {scale}')

    def get_vertical_scale(self, channel, math = False):
        '''
        Returns the vertical scale in V/div of the given channel
        channel: integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            return float(self.comm(f"MATH{channel}:VERT:SCA?"))
        else:
            return float(self.comm(f"CH{channel}:SCA?"))

    def set_vertical_position(self, channel, position, math = False):
        '''
        Sets the vertical position for a given channel in V
        channel : integer of the channel
        position : Veritcal position in V
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            self.comm(f"MATH{channel}:VERT:POS {position}")
        else:
            self.comm(f"CH{channel}:POS {position}")

    def get_vertical_position(self, channel, math = False):
        '''
        Returns the vertical position for a given channel in V
        channel : integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            return float(self.comm(f"MATH{channel}:VERT:POS?"))
        else:
            return float(self.comm(f"CH{channel}:POS?"))

    def set_termination(self, channel, termination):
        '''
        Sets the termination of the channel
        channel : integer of the channel
        termination : Either 50 or 1e6
        '''
        if termination not in [50, 1e6]:
            raise ValueError('Unknown Termination Value. Set to either 50 or 1e6')
        self.comm(f"CH{channel}:TER {termination}")

    def get_termination(self, channel):
        '''
        Returns the termination of the channel
        channel : integer of the channel
        '''
        return float(self.comm(f"CH{channel}:TER?"))

    def set_channel_state(self, channel, state, math = False):
        '''
        Sets the display state of the specified channel
        channel : integer of the channel
        state : Boolean or 1/0 integer describing the display state of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            if state:
                self.comm(f"SEL:MATH{channel} ON")
            else:
                self.comm(f"SEL:MATH{channel} OFF")
        else:
            if state:
                self.comm(f"SEL:CH{channel} ON")
            else:
                self.comm(f"SEL:CH{channel} OFF")

    def get_channel_state(self, channel, math = False):
        '''
        Returns the display state of the specified channel as 1 or 0
        channel : integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            return int(self.comm(f"SEL:MATH{channel}?"))
        else:
            return int(self.comm(f"SEL:CH{channel}?"))

    def set_channel_deskew(self, channel, deskew):
        '''
        Sets the deskew value of the given channel
        channel : integer of the channel
        deskew :  time value (in seconds) to shift the channel between -75ns and 75ns
        '''
        if deskew < -75e-12 or deskew > 75e-12:
            raise ValueError("Deskew must be bewteen +/- 75ns represented in seconds")
        self.comm(f"CH{channel}:DESKEW {deskew}")
        
    def get_channel_deskew(self, channel):
        '''
        Returns the deskew value of the given channel in seconds
        channel : integer of the channel
        '''
        return float(self.comm(f"CH{channel}:DESKEW?"))

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
        self.comm(f"MATH{channel}:DEFINE CH{channel1}{operation}CH{channel2}")
        self.comm(f"SELECT:MATH{channel} ON")

    def get_math(self, channel):
        '''
        Returns the string representation of the math equation
        '''
        return self.comm(f'MATH{channel}:DEFINE?')

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
            for i in range(1,8):
                if int(self.comm(f"MEASU:MEAS{i}:STATE?")):
                    measurement_number = i + 1

        if math:
            channel_type = 'MATH'
        else:
            channel_type = 'CH'

        if mtype.lower() in 'amplitude':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP AMPL; STATE ON')
        elif mtype.lower() in 'rise':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP RISE; STATE ON')
        elif mtype.lower() in 'fall':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP FALL; STATE ON')
        elif mtype.lower() in 'pk2pk':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP PK2PK; STATE ON')
        elif mtype.lower() in 'frequency':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP FREQ; STATE ON')
        elif mtype.lower() in 'pduty':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP PDUTY; STATE ON')
        elif mtype.lower() in 'nduty':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP NDUTY; STATE ON')
        elif mtype.lower() in 'high':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP HIGH; STATE ON')
        elif mtype.lower() in 'low':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP LOW; STATE ON')
        elif mtype.lower() in 'max':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP MAX; STATE ON')
        elif mtype.lower() in 'min':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP MINI; STATE ON')
        elif mtype.lower() in 'mean':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP MEAN; STATE ON')
        elif mtype.lower() in 'over':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP POV; STATE ON')
        elif mtype.lower() in 'under':
            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; TYP NOV; STATE ON')
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

            self.comm(f'MEASU:MEAS{measurement_number}:SOU1 {channel_type}{channel}; SOU2 {channel_type2}{channel2};TYP DELAY; STATE ON')
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
        if not int(self.comm(f"MEASU:MEAS{measurement_number}:STATE?")):
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
        Returns the last captured value of the measurement
        measurement_number : integer of measurement
        '''
        return float(f"MEASU:MEAS{measurement_number}?")

    def meas_mean_measurement(self,measurement_number):
        '''
        Returns the mean of the measurement
        measurement_number : integer of measurement
        '''
        return float(self.comm(f'MEASU:MEAS{measurement_number}:MEAN?'))

    def meas_max_measurement(self,measurement_number):
        """
        Returns the max of the measurement
        measurement_number : integer of measurement
        """
        return float(self.comm(f"MEASU:MEAS{measurement_number}:MAX?"))

    def meas_min_measurement(self,measurement_number):
        """
        Returns the min of the measurement
        measurement_number : integer of measurement
        """
        return float(self.comm(f"MEASU:MEAS{measurement_number}:MINI?"))   

    def set_measurement_reference(self, measurement_number, reference_type, threshold, level):
        '''
        Sets the measurement reference position
        measurement_number : integer of measurement
        reference_type : 'percent' or 'absolute'
        threshold : 'high', 'mid', or 'low'
        level : a percentage if reference type is 'percent' or a voltage if reference type is 'absolute'
        '''
        if reference_type.upper() in 'PERCENT':
            self.comm(f'MEASU:MEAS{measurement_number}:REFLevel:METHod PERcent')
            self.comm(f"MEASU:MEAS{measurement_number}:REFLevel:PERCENT:{threshold.upper()} {level}")
            
        elif reference_type.upper() in 'ABSOLUTE':
            self.comm(f'MEASU:MEAS{measurement_number}:REFLevel:METHod ABSolute')
            self.comm(f"MEASU:MEAS{measurement_number}:REFLevel:ABS:{threshold.upper()} {level}")

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
            ret['level_high'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevel:PERCENT:HIGH?"))
            ret['level_mid'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevel:PERCENT:MID?"))
            ret['level_low'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevel:PERCENT:LOW?"))    
        elif reference_type.lower() in 'absolute':
            ret['reference_type'] = 'absolute'
            ret['level_high'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevel:ABSOLUTE:HIGH?"))
            ret['level_mid'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevel:ABSOLUTE:MID?"))
            ret['level_low'] = float(self.comm(f"MEASU:MEAS{measurement_number}:REFLevel:ABSOLUTE:LOW?"))  
        else:
            ret['reference_type'] = 'unknown'
            ret['level_high'] = 'unknown'
            ret['level_mid'] = 'unknown'
            ret['level_low'] = 'unknown'
        
    def reset_measurement_statistics(self):
        '''
        Resets the measurement stats
        '''
        self.comm("MEASU:STATI:COUNT RESET")

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
            self.comm(f"TRIG:{trigger.upper()}:EDGE:SOUR MATH{channel}")
        else:
            self.comm(f"TRIG:{trigger.upper()}:EDGE:SOUR CH{channel}")

    def set_trigger_level(self, trigger, level):
        """
        Returns trigger level in volts
        trigger : 'a' or 'b'
        level : voltage value (V) or "center"
        """ 
        if level.lower() in 'center':
            self.comm(f"TRIG:{trigger.upper()}:LEV SETL")
        else:
            self.comm(f"TRIG:{trigger.upper()}:LEV {level}")
    
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

    def get_trigger_source(self, trigger):
        """
        Returns trigger source
        trigger : 'a' or 'b'
        """
        return self.comm(f"TRIG:{trigger.upper()}:EDGE:SOUR?")[:-1]

    def get_trigger_level(self, trigger):
        """
        Returns trigger level in volts
        trigger : 'a' or 'b'
        """ 
        return float(self.comm(f"TRIG:{trigger.upper()}:LEV?"))
    
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
        Gets the plot from scope and saves it to the filename (full path) as a png
        filename : full path of file to save image to (must end in .png)
        invert : boolean as to whether or not the color of the image is inverted
        '''
        self.comm("EXPORT:FORMAT PNG")
        
        if invert:
            self.comm("EXPORT:IMAG INKS")
        else:
            self.comm("EXPORT:IMAG NORM")
        
        self.comm("HARDCOPY:PORT FILE")
        self.comm("HARDCOPY:FILENAME 'C:\temp.png'")
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

    def get_trace_data(channel, math = False):
        '''
        Returns the data points of the channel as a list of floats
        channel : integer of channel (0 = x data)
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        ydata = []
        xdata = []

        if math:
            self.comm(f"DATA:SOU MATH{channel}")
        elif channel == 0:
            self.comm(f"DATA:SOU CH1")
        else:
            self.comm(f"DATA:SOU CH{channel}")
        self.comm(f"DATA:ENC ASCI")
        self.comm("HEAD 0")
        y_mult = float(self.comm("WFMO:YMULT?"))
        y_offs = float(self.comm("WFMO:YOFF?"))
        y_zero = float(self.comm("WFMO:YZERO?"))
        x_zero = float(self.comm("WFMO:XZERO?"))
        x_inc = float(self.comm("WFMO:XINCR?"))
        x_ptoffset = float(self.comm("WFMO:PT_OFF?"))
        xy_trace = [int(a) for a in self.comm("CURV?").split(",")]

        for x,y in enumerate(xy_trace):
            ydata.append((float(y)-y_offs)*y_mult + y_zero)
            xdata.append((float(x)-x_ptoffset)*x_inc + x_zero)

        if channel == 0:
            return xdata
        else:
            return ydata

    def get_trace_to_file(self, channel, filename, math = False):
        """
        Gets the trace data and saves it to the given txt file in two data columns
        channel : integer of channel
        filename : full path of file to save image to (must end in .txt)
        math : boolean as to whether or not the channel integer refers to a math channel
        """
        ydata = []
        xdata = []

        if math:
            self.comm(f"DATA:SOU MATH{channel}")
        else:
            self.comm(f"DATA:SOU CH{channel}")
        self.comm(f"DATA:ENC ASCI")
        self.comm("HEAD 0")
        y_mult = float(self.comm("WFMO:YMULT?"))
        y_offs = float(self.comm("WFMO:YOFF?"))
        y_zero = float(self.comm("WFMO:YZERO?"))
        x_zero = float(self.comm("WFMO:XZERO?"))
        x_inc = float(self.comm("WFMO:XINCR?"))
        x_ptoffset = float(self.comm("WFMO:PT_OFF?"))
        xy_trace = [int(a) for a in self.comm("CURV?").split(",")]

        for x,y in enumerate(xy_trace):
            ydata.append((float(y)-y_offs)*y_mult + y_zero)
            xdata.append((float(x)-x_ptoffset)*x_inc + x_zero)

        with open(filename, 'w') as f:
            for col1,col2 in zip(xdata,ydata):
                f.writelines(f"{col1}\t{col2}\n")


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
            self.comm("ACQ:STOPA SEQ")
        elif mode.upper() in "RUN":
            self.comm("ACQ:STOPA RUNST")
        else:
            raise ValueError('Unknown mode value. Please use either "single" or "run".') 

    def get_run_mode(self):
        """
        Gets the waveform acquisition run mode. Returns a string 'RUN' or 'SINGLE'
        """
        return self.comm("ACQ:STOPA?")[:-1]

    def set_run_state(self, state):
        """
        Starts or stops the acquisition. Call this after setting set_run_mode('Single').
        state : boolean or 1/0
        """
        if state:
            self.comm("ACQ:STATE ON")
        else:
            self.comm("ACQ:STATE OFF")

    def get_run_state(self):
        """
        Gets the acquisition state
        """
        return self.comm("ACQ:STATE?")

    def set_acquisition_mode(self, mode):
        """
        Sets the acquisition type
        mode = sample, peakdet, hires, average, envelope
        """
        if mode.lower() in "sample":
            self.comm(f'ACQ:MOD SAM')
        elif mode.lower() in "peakdet":
            self.comm(f'ACQ:MOD PEAK')
        elif mode.lower() in "hires":
            self.comm(f'ACQ:MOD HIR')
        elif mode.lower() in "average":
            self.comm(f'ACQ:MOD AVE')
        elif mode.lower() in "envelope":
            self.comm(f'ACQ:MOD ENV')
        else:
            raise ValueError('Unknown acquisition mode. Must be set to [sample, peakdet, hires, average, envelope]')

    def get_acquisition_mode(self):
        """
        Returns the acquisition mode as a string
        """
        mode = self.comm(f'ACQ:MOD?')[:-1]
        if mode.lower() in "sample":
            return 'sample'
        elif mode.lower() in "peakdet":
            return 'peakdet'
        elif mode.lower() in "hires":
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
        self.comm(f"ACQ:NUMAVG {count}")

    def get_acquisition_average_count(self):
        """
        Returns number of waveforms selected for average
        """
        return int(self.comm("ACQ:NUMAVG?"))

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Run/Acquisition Methods      '''
    '''''''''''''''''''''''''''''''''''''''''''''''' 