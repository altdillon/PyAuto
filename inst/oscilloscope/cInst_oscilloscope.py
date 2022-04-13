from cInst import cInst
import time

class cInst_oscilloscope(cInst):
    '''
    oscilloscope main class
    '''

    def set_auto_scale(self):
        """Performs front panel equivalent of AUTOSET"""
        self.comm("AUTOS EXEC")


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

    def set_time_delay(self):
        pass

    def get_time_delay(self):
        pass

    def set_sampling_rate(self, rate = 20e9):
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

    def set_record_length(self, record_length = 1000):
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

    def set_horizontal_mode(self, mode = 'AUTO'):
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
        return float(self.comm(f"{channel}:DESKEW?"))


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


    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Measurement Methods          '''
    ''''''''''''''''''''''''''''''''''''''''''''''''

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Unedited Below               '''
    ''''''''''''''''''''''''''''''''''''''''''''''''


    def meas_mean_measurement(self,measurement_number = 1):
        '''
        returns mean measurement
        '''
        return float(self.comm('MEASU:MEAS{}:Mean?'.format(measurement_number)))

    def meas_max_measurement(self,measurement_number = 1):
        """
        Returns the max value of the measurement since stat reset
        """
        return float(self.comm(f"MEASU:MEAS{measurement_number}:MAX?"))

    def meas_min_measurement(self,measurement_number = 1):
        """
        Returns the max value of the measurement since stat reset
        """
        return float(self.comm(f"MEASU:MEAS{measurement_number}:MINI?"))        

    def get_plot(self, filename, invert = False):
        '''
        Gets plot from scope and save it to the filename (full path) as a png passed to the function
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

        with open(filename,'wb') as fp:
            fp.write(raw)


    def set_run_mode(self,mode = "RUN"):
        """
        Set the waveform acquisition run mode
        mode = 'RUN' or 'SINGLE'
        """
        if mode.upper() in "SINGLE":
            self.comm("ACQ:STOPA SEQ")
            #self.comm("ACQ:STATE OFF")
        elif mode.upper() in "RUN":
            self.comm("ACQ:STOPA RUNST")
            #self.comm("ACQ:STATE ON")
        else:
            raise ValueError('Unknown mode value. Please use either "SINGLE" or "RUN".') 

    def get_run_mode(self):
        """
        Set the waveform acquisition run mode. Returns a string 'RUN' or 'SINGLE'
        """
        return self.comm("ACQ:STOPA?")

    def set_run_state(self, state = 1):
        """
        Start or stop acquisition. Call this after setting set_run_mode('Single').
        """
        if state:
            self.comm("ACQ:STATE ON")
        else:
            self.comm("ACQ:STATE OFF")

    def set_run_state(self, state = 1):
        """
        Get acquisition state
        """
        self.comm("ACQ:STATE?")