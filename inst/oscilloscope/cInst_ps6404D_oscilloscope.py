from cInst_oscilloscope import cInst_oscilloscope
import ctypes, ctypes.util
import os
import numpy as np


''''''''''''''''''''''''''''''''''''''''''''''''
'''             Defining Constants           '''
'''''''''''''''''''''''''''''''''''''''''''''''' 
#PS6000_RANGE
PS6000A_10MV = ctypes.c_int(0)
PS6000_20MV = ctypes.c_int(1)
PS6000_50MV = ctypes.c_int(2)
PS6000_100MV = ctypes.c_int(3)
PS6000_200MV = ctypes.c_int(4)
PS6000_500MV = ctypes.c_int(5)
PS6000_1V = ctypes.c_int(6)
PS6000_2V = ctypes.c_int(7)
PS6000_5V = ctypes.c_int(8)
PS6000_10V = ctypes.c_int(9)
PS6000_20V = ctypes.c_int(10)
PS6000_50V = ctypes.c_int(11)
PS6000_MAX_RANGES = ctypes.c_int(12)
list_ranges = [PS6000A_10MV,PS6000_20MV,PS6000_50MV,PS6000_100MV,PS6000_200MV,PS6000_500MV,PS6000_1V,PS6000_2V,PS6000_5V,PS6000_10V,PS6000_20V,PS6000_50V]
list_scales = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]

#PS6000_CHANNEL
PS6000_CHANNEL_A = ctypes.c_int(0)
PS6000_CHANNEL_B = ctypes.c_int(1)
PS6000_CHANNEL_C = ctypes.c_int(2)
PS6000_CHANNEL_D = ctypes.c_int(3)
PS6000_EXTERNAL = PS6000_MAX_CHANNELS = ctypes.c_int(4)
PS6000_TRIGGER_AUX = ctypes.c_int(5)
PS6000_MAX_TRIGGER_SOURCES = ctypes.c_int(6)

#PS6000_COUPLING
PS6000_AC = ctypes.c_int(0)
PS6000_DC_1M = ctypes.c_int(1)
PS6000_DC_50R = ctypes.c_int(2)

#PS6000_BANDWIDTH_LIMITER
PS6000_BW_FULL = ctypes.c_int(0)
PS6000_BW_20MHZ = ctypes.c_int(1)
PS6000_BW_25MHZ = ctypes.c_int(2)

#PS6000_RATIO_MODE
PS6000_RATIO_MODE_NONE = ctypes.c_int(0)
PS6000_RATIO_MODE_AGGREGATE = ctypes.c_int(1)
PS6000_RATIO_MODE_AVERAGE = ctypes.c_int(2)
PS6000_RATIO_MODE_DECIMATE = ctypes.c_int(4)
PS6000_RATIO_MODE_DISTRIBUTION = ctypes.c_int(8)

#PS6000_TIME_UNITS
PS6000_FS = ctypes.c_int(0)
PS6000_PS = ctypes.c_int(1)
PS6000_NS = ctypes.c_int(2)
PS6000_US = ctypes.c_int(3)
PS6000_MS = ctypes.c_int(4)
PS6000_S = ctypes.c_int(5)
PS6000_MAX_TIME_UNITS = ctypes.c_int(6)

#PS6000_TRIGGER_STATE
PS6000_CONDITION_DONT_CARE = ctypes.c_int(0)
PS6000_CONDITION_TRUE = ctypes.c_int(1)
PS6000_CONDITION_FALSE = ctypes.c_int(2)
PS6000_CONDITION_MAX = ctypes.c_int(3)

#PS6000_THRESHOLD_DIRECTION
PS6000_ABOVE = PS6000_INSIDE = ctypes.c_int(0)
PS6000_BELOW = PS6000_BELOW = ctypes.c_int(1)
PS6000_RISING = PS6000_ENTER = PS6000_NONE = ctypes.c_int(2)
PS6000_FALLING = PS6000_EXIT = ctypes.c_int(3)
PS6000_RISING_OR_FALLING = PS6000_ENTER_OR_EXIT = ctypes.c_int(4)
PS6000_ABOVE_LOWER = ctypes.c_int(5)
PS6000_BELOW_LOWER = ctypes.c_int(6)
PS6000_RISING_LOWER = ctypes.c_int(7)
PS6000_FALLING_LOWER = ctypes.c_int(8)
PS6000_POSITIVE_RUNT = ctypes.c_int(9)
PS6000_NEGATIVE_RUNT = ctypes.c_int(10)
    
#PS6000_THRESHOLD_MODE
PS6000_LEVEL = ctypes.c_int(0)
PS6000_WINDOW = ctypes.c_int(1)

#PS6000_PULSE_WIDTH_TYPE
PS6000_PW_TYPE_NONE = ctypes.c_int(0)
PS6000_PW_TYPE_LESS_THAN = ctypes.c_int(1)
PS6000_PW_TYPE_GREATER_THAN = ctypes.c_int(2)
PS6000_PW_TYPE_IN_RANGE = ctypes.c_int(3)
PS6000_PW_TYPE_OUT_OF_RANGE = ctypes.c_int(4)

#PICO_INFO
PICO_DRIVER_VERSION = ctypes.c_int(0)
PICO_USB_VERSION = ctypes.c_int(1)
PICO_HARDWARE_VERSION = ctypes.c_int(2)
PICO_VARIANT_INFO = ctypes.c_int(3)
PICO_BATCH_AND_SERIAL = ctypes.c_int(4)
PICO_CAL_DATE = ctypes.c_int(5)
PICO_KERNAL_VERSION = ctypes.c_int(6)
PICO_DIGITAL_HARDWARE_VERSION = ctypes.c_int(7)
PICO_ANALOGUE_HARDWARE_VERSION = ctypes.c_int(8)
PICO_FIRMWARE_VERSION_1 = ctypes.c_int(9)
PICO_FIREWARE_VERSION_2 = ctypes.c_int(10)

#Sampling Intervals
lower_sampling = [0.0000000002, 0.0000000004, 0.0000000008, 0.0000000016, 0.0000000032]


class cInst_ps6404D_oscilloscope(cInst_oscilloscope):

    '''
    TBD

    Available, but not used, dll functions:
    [ps6000GetUnitInfo, ps6000FlashLed, ps6000MemorySegments, ps6000SetSigGenArbitrary,
    ps6000SetSigGenBuiltIn, ps6000SetSigGenBuiltInV2, ps6000SetSigGenPropertiesArbitrary,
    ps6000SetSigGenPropertiesBuiltIn, ps6000SigGenFrequencyToPhase, ps6000SigGenArbitraryMinMaxValues,
    ps6000SigGenSoftwareControl, ps6000PingUnit]
    '''

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             cInst Methods                '''
    '''''''''''''''''''''''''''''''''''''''''''''''' 

    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'oscilloscope'
        self.ps6000 = ctypes.WinDLL(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ps6000.dll'))

        enabled = ctypes.c_uint16(0)
        #self.ps6000["ps6000SetChannel"](self.inst, PS6000_CHANNEL_A, enabled, PS6000_DC_1M, PS6000_1V, 0, PS6000_BW_FULL)
        self.ps6000["ps6000SetChannel"](self.inst, PS6000_CHANNEL_B, enabled, PS6000_DC_1M, PS6000_1V, 0, PS6000_BW_FULL)
        self.ps6000["ps6000SetChannel"](self.inst, PS6000_CHANNEL_C, enabled, PS6000_DC_1M, PS6000_1V, 0, PS6000_BW_FULL)
        self.ps6000["ps6000SetChannel"](self.inst, PS6000_CHANNEL_D, enabled, PS6000_DC_1M, PS6000_1V, 0, PS6000_BW_FULL)
        self.active_channels = [1]

        self.time_scale = None
        self.trigger_delay = 0
        self.sampling_rate = None
        self.record_length = None

        self.set_channel = {0: {'channel': PS6000_CHANNEL_A, 
                                'enabled': ctypes.c_uint16(1),
                                'coupling': PS6000_DC_1M,
                                'range': PS6000_50MV,
                                'offset': ctypes.c_float(0),
                                'bandwidth': PS6000_BW_FULL},
                            1: {'channel': PS6000_CHANNEL_B, 
                                'enabled': ctypes.c_uint16(0),
                                'coupling': PS6000_DC_1M,
                                'range': PS6000_50MV,
                                'offset': ctypes.c_float(0),
                                'bandwidth': PS6000_BW_FULL},
                            2: {'channel': PS6000_CHANNEL_C, 
                                'enabled': ctypes.c_uint16(0),
                                'coupling': PS6000_DC_1M,
                                'range': PS6000_50MV,
                                'offset': ctypes.c_float(0),
                                'bandwidth': PS6000_BW_FULL},
                            3: {'channel': PS6000_CHANNEL_D, 
                                'enabled': ctypes.c_uint16(0),
                                'coupling': PS6000_DC_1M,
                                'range': PS6000_50MV,
                                'offset': ctypes.c_float(0),
                                'bandwidth': PS6000_BW_FULL}}
        
    def comm(self,command):
        raise ValueError('Comm is not available for non-visa devices. Use the library (.ps6000) and the handle (.inst) to make a raw command.')

    def set_address(self, address):
        pass

    def launch_gui(self):
        pass

    def reset(self):
        pass

    def disconnect(self):
        self.ps6000['ps6000CloseUnit'](self.inst)


    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             cInst Methods                '''
    '''''''''''''''''''''''''''''''''''''''''''''''' 

    def set_auto_scale(self):
        """Performs front panel equivalent of AUTOSET"""
        '''I can kinda do this??'''
        raise ValueError('set_auto_scale is not available for non-visa devices. Use the library (.ps6000) and the handle (.inst) to make a raw command.')

    def set_persistence(self, state):
        '''
        Sets the state of persistence (resets if already on)
        state : boolean as to whther or not persistence is on
        '''
        raise ValueError('set_persistence is not available for non-visa devices. Use the library (.ps6000) and the handle (.inst) to make a raw command.')

    ''''''''''''''''''''''''''''''''''''''''''''''''
    '''             Horizontal Methods           '''
    ''''''''''''''''''''''''''''''''''''''''''''''''

    def set_time_scale(self, time_scale):
        '''
        sets horizontal scale (seconds/division)
        '''
        #self.comm(f'HORIZONTAL:SCA {time_scale}')

        #setting timebase (time between samples) to 0 (representing 200ps, or fastest possible)
        #then calculating noSamples to achieve desired time scale
        #then see what happens?

        timebase = 0
        noSamples = int(round(time_scale*10/0.0000000002, 0))
        while noSamples > 2000000000:
            timebase+=1
            if timebase < 5:
                noSamples = int(round(time_scale*10/((2**timebase)/5000000000), 0))*len(self.active_channels)
            else:
                noSamples = int(round(time_scale*10/((timebase-4)/156250000), 0))*len(self.active_channels)

        timebase = ctypes.c_uint32(timebase)
        noSamples = ctypes.c_uint32(noSamples)
        time_interval = ctypes.c_float()
        oversample = ctypes.c_uint16(0)
        maxSamples = ctypes.c_uint32()
        segmentIndex = ctypes.c_uint32(0)

        self.ps6000["ps6000GetTimebase2"](self.inst, timebase, noSamples, ctypes.byref(time_interval), oversample, ctypes.byref(maxSamples), segmentIndex)

        self.time_scale = time_interval.value * noSamples.value / (10 * len(self.active_channels) * 1000000000)
        self.sampling_rate = 1 / time_interval.value
        self.record_length = noSamples.value

    def get_time_scale(self):
        """
        Returns the time base(second per division)
        """
        if self.time_scale == None:
            raise ValueError('Time scale not yet set.')
        else:
            return self.time_scale

    def set_time_delay(self, delay):
        '''
        Sets the horizontal delay in seconds
        I'm not certain this is right...
        '''
        self.trigger_delay = delay
        trigger_delay = ctypes.c_uint32(int(self.get_sampling_rate()*delay))
        self.ps6000["ps6000SetTriggerDelay"](self.inst, trigger_delay)

    def get_time_delay(self):
        '''
        Returns the horizontal delay in seconds
        '''
        return self.trigger_delay

    def set_sampling_rate(self, rate):
        """
        Set the sampling rate of the scope. Based on the time axis duration, the value set may be adjusted automatically by the scope
        rate : sampling rate in samples/second
        """
        time_interval = 1/rate
        if time_interval < 0.000000048: #48 ns
            timebase = ctypes.c_uint32(min(range(len(lower_sampling)), key = lambda i: abs(lower_sampling[i]-time_interval)))
        else:
            timebase = ctypes.c_uint32(int(time_interval*156250000)+4)

        noSamples = ctypes.c_uint32(2000000000) #2GS
        time_interval = ctypes.c_float()
        oversample = ctypes.c_uint16(0)
        maxSamples = ctypes.c_uint32()
        segmentIndex = ctypes.c_uint32(0)

        self.ps6000["ps6000GetTimebase2"](self.inst, timebase, noSamples, ctypes.byref(time_interval), oversample, ctypes.byref(maxSamples), segmentIndex)

        self.time_scale = time_interval.value * noSamples.value / (10 * len(self.active_channels) * 1000000000)
        self.sampling_rate = 1 / time_interval.value
        self.record_length = noSamples.value

    def get_sampling_rate(self):
        """
        Returns set sampling rate
        """
        if self.sampling_rate == None:
            raise ValueError('Time scale not yet set.')
        else:
            return self.sampling_rate

    def set_record_length(self, record_length):
        """
        Sets the number of points that can be acquired per waveform with current time base and sampling rate setting
        record_length = numeric value
        """
        if self.time_scale == None or self.sampling_rate == None:
            raise ValueError('Time scale not yet set.')

        time_interval = 1/self.sampling_rate
        if time_interval < 0.000000048: #48 ns
            timebase = ctypes.c_uint32(min(range(len(lower_sampling)), key = lambda i: abs(lower_sampling[i]-time_interval)))
        else:
            timebase = ctypes.c_uint32(int(time_interval*156250000)+4)

        noSamples = ctypes.c_uint32(record_length) #2GS
        time_interval = ctypes.c_float()
        oversample = ctypes.c_uint16(0)
        maxSamples = ctypes.c_uint32()
        segmentIndex = ctypes.c_uint32(0)

        self.ps6000["ps6000GetTimebase2"](self.inst, timebase, noSamples, ctypes.byref(time_interval), oversample, ctypes.byref(maxSamples), segmentIndex)

        self.time_scale = time_interval.value * noSamples.value / (10 * len(self.active_channels) * 1000000000)
        self.record_length = noSamples.value

    def get_record_length(self):
        """
        Returns the current record length
        """
        if self.record_length == None:
            raise ValueError('Time scale not yet set.')
        else:
            return self.record_length

    def set_horizontal_mode(self, mode):
        """
        Sets the mode to determine correlation between sampling rate, time base and record length
        mode = 'Auto'       Auto mode attempts to keep record length constant as you change the time per division setting. Record length is read only
             = 'Constant'   Constant mode attempts to keep sample rate constant as you change the time per division setting. Record length is read only.
             = 'Manual'     Manual mode lets you change sample mode and record length. Time per division or Horizontal scale is read only
        """
        raise ValueError('horizontal_mode is not available for non-visa devices. Use the library (.ps6000) and the handle (.inst) to make a raw command.')

    def get_horizontal_mode(self):
        """
        Return the horizontal mode. This mode determine correlation between sampling rate, time base and record length 
        """
        raise ValueError('horizontal_mode is not available for non-visa devices. Use the library (.ps6000) and the handle (.inst) to make a raw command.')


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
            raise ValueError('Cannot set math remotely')

        self.set_channel[channel]['range'] = list_ranges[min(range(len(list_scales)), key = lambda i: abs(list_scales[i]-scale))]
        self.ps6000["ps6000SetChannel"](self.inst,
                                        self.set_channel[channel]['channel'],
                                        self.set_channel[channel]['enabled'],
                                        self.set_channel[channel]['coupling'],
                                        self.set_channel[channel]['range'],
                                        self.set_channel[channel]['offset'],
                                        self.set_channel[channel]['bandwidth'])

    def get_vertical_scale(self, channel, math = False):
        '''
        Returns the vertical scale in V/div of the given channel
        channel: integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            raise ValueError('Cannot get math remotely')
        return list_scales[self.set_channel[channel]['range'].value]

    def set_vertical_position(self, channel, position, math = False):
        '''
        Sets the vertical position for a given channel in V
        channel : integer of the channel
        position : Veritcal position in V
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            raise ValueError('Cannot set math remotely')

        maximumVoltage = ctypes.c_float()
        minimumVoltage = ctypes.c_float()
        stat = self.ps6000["ps6000GetAnalogueOffset"](self.inst, self.set_channel[channel]['range'], self.set_channel[channel]['coupling'], ctypes.byref(maximumVoltage), ctypes.byref(minimumVoltage))

        if not (minimumVoltage.value < position < maximumVoltage.value):
            raise ValueError(f'Position out of range {minimumVoltage.value} to {maximumVoltage.value}')

        self.set_channel[channel]['offset'] = ctypes.c_float(position)
        self.ps6000["ps6000SetChannel"](self.inst,
                                        self.set_channel[channel]['channel'],
                                        self.set_channel[channel]['enabled'],
                                        self.set_channel[channel]['coupling'],
                                        self.set_channel[channel]['range'],
                                        self.set_channel[channel]['offset'],
                                        self.set_channel[channel]['bandwidth'])

    def get_vertical_position(self, channel, math = False):
        '''
        Returns the vertical position for a given channel in V
        channel : integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            raise ValueError('Cannot get math remotely')
        
        return self.set_channel[channel]['offset'].value

    def set_termination(self, channel, termination):
        '''
        Sets the termination of the channel
        channel : integer of the channel
        termination : Either 50 or 1e6
        '''

        #NOTE: AC coupling not used

        if termination not in [50, 1e6]:
            raise ValueError('Unknown Termination Value. Set to either 50 or 1e6')
        
        if termination == 50:
            self.set_channel[channel]['coupling'] = PS6000_DC_50R
        else:
            self.set_channel[channel]['coupling'] = PS6000_DC_1M

        self.ps6000["ps6000SetChannel"](self.inst,
                                        self.set_channel[channel]['channel'],
                                        self.set_channel[channel]['enabled'],
                                        self.set_channel[channel]['coupling'],
                                        self.set_channel[channel]['range'],
                                        self.set_channel[channel]['offset'],
                                        self.set_channel[channel]['bandwidth'])

    def get_termination(self, channel):
        '''
        Returns the termination of the channel
        channel : integer of the channel
        '''

        #NOTE: AC coupling not used

        if self.set_channel[channel]['coupling'].value == 1:
            return 1e6
        else:
            return 50

    def set_channel_state(self, channel, state, math = False):
        '''
        Sets the display state of the specified channel
        channel : integer of the channel
        state : Boolean or 1/0 integer describing the display state of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            raise ValueError('Cannot set math remotely')
        else:
            if state:
                self.set_channel[channel]['enabled'] = ctypes.c_uint16(1)
            else:
                self.set_channel[channel]['enabled'] = ctypes.c_uint16(0)

        self.ps6000["ps6000SetChannel"](self.inst,
                                        self.set_channel[channel]['channel'],
                                        self.set_channel[channel]['enabled'],
                                        self.set_channel[channel]['coupling'],
                                        self.set_channel[channel]['range'],
                                        self.set_channel[channel]['offset'],
                                        self.set_channel[channel]['bandwidth'])

    def get_channel_state(self, channel, math = False):
        '''
        Returns the display state of the specified channel as 1 or 0
        channel : integer of the channel
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            raise ValueError('Cannot get math remotely')
        else:
            return self.set_channel[channel]['enabled'].value

    def set_channel_deskew(self, channel, deskew):
        '''
        Sets the deskew value of the given channel
        channel : integer of the channel
        deskew :  time value (in seconds) to shift the channel between -75ns and 75ns
        '''
        raise ValueError('PicoScope cannot set skew')
        
    def get_channel_deskew(self, channel):
        '''
        Returns the deskew value of the given channel in seconds
        channel : integer of the channel
        '''
        raise ValueError('PicoScope cannot get skew')

    def set_math(self, channel1, channel2, operation, channel = None):
        """
        Sets up a math operation ({channel1} {operation} {channel2})
        channel1 : integer of first channel in equation
        channel2 : integer of second channel in equation
        operation : '+' or '-'
        channel : integer of math channel to set up (if unspecified, adds a new math signal)
        """
        raise ValueError('Cannot set math remotely')

    def get_math(self, channel):
        '''
        Returns the string representation of the math equation
        '''
        raise ValueError('Cannot get math remotely')

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
            raise ValueError("mtype must be one of the following:  ['amplitude', 'high', 'low', 'max', 'min', 'mean', 'pk2pk', 'under', 'over', 'rise', 'fall', 'pduty', 'nduty', 'frequency', 'delay']")

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
            ret['math2'] = 'MATH' in source.upper()
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
        ret['math'] = 'MATH' in source.upper()
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
        return ret
        
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
        raise ValueError('Depricated')
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

    def get_trace_data(self, channel, math = False):
        '''
        Returns the data points of the channel as a list of floats
        channel : integer of channel (0 = x data)
        math : boolean as to whether or not the channel integer refers to a math channel
        '''
        if math:
            raise ValueError('Cannot get math remotely')

        if channel == 0:
            return list(np.linspace(0, (self.record_length -1) / self.sampling_rate , self.record_length))

        bufferMax = (ctypes.c_int16 * self.record_length)()
        bufferMin = (ctypes.c_int16 * self.record_length)()
        self.ps6000["ps6000SetDataBuffers"](self.inst,
                                            self.set_channel[channel]['channel'],
                                            ctypes.byref(bufferMax),
                                            ctypes.byref(bufferMin),
                                            ctypes.c_uint32(self.record_length),
                                            PS6000_RATIO_MODE_NONE)

        overflow = ctypes.c_int16()
        cmaxSamples = ctypes.c_int32(self.record_length)
        self.ps6000["ps6000GetValues"](self.inst, 0, ctypes.byref(cmaxSamples), 1, PS6000_RATIO_MODE_NONE, 0, ctypes.byref(overflow))

        maxADC = 32512
        vRange = list_scales[self.set_channel[channel]['range'].value]*10
        return [(x.value * vRange) / maxADC for x in bufferMax]

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









'''
    """ PICO_STATUS ps6000SetChannel
        (
            int16_t                   handle,
            PS6000_CHANNEL            channel,
            int16_t                   enabled,
            PS6000_COUPLING           type,
            PS6000_RANGE              range,
            float                     analogueOffset,
            PS6000_BANDWIDTH_LIMITER  bandwidth
        ); """
    make_symbol(ldlib, "SetChannel", "ps6000SetChannel", c_uint32,
                [c_int16, c_int32, c_int16, c_int32, c_int32, c_float, c_int32])

    """ PICO_STATUS ps6000GetTimebase
        (
            int16_t   handle,
            uint32_t  timebase,
            uint32_t  noSamples,
            int32_t  *timeIntervalNanoseconds,
            int16_t   oversample,
            uint32_t *maxSamples,
            uint32_t  segmentIndex
        ); """

    """ PICO_STATUS ps6000GetTimebase2
        (
            int16_t   handle,
            uint32_t  timebase,
            uint32_t  noSamples,
            float    *timeIntervalNanoseconds,
            int16_t   oversample,
            uint32_t *maxSamples,
            uint32_t  segmentIndex
        ); """
    make_symbol(ldlib, "GetTimebase", "ps6000GetTimebase2", c_uint32,
                [c_int16, c_uint32, c_uint32, c_void_p, c_int16, c_void_p, c_uint32])

    

    

   

    
   

    """ PICO_STATUS ps6000SetSimpleTrigger
        (
            int16_t                     handle,
            int16_t                     enable,
            PS6000_CHANNEL              source,
            int16_t                     threshold,
            PS6000_THRESHOLD_DIRECTION  direction,
            uint32_t                    delay,
            int16_t                     autoTrigger_ms
        ); """
    make_symbol(ldlib, "SetSimpleTrigger", "ps6000SetSimpleTrigger", c_uint32,
                [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16])

    """ PICO_STATUS ps6000SetEts
        (
            int16_t          handle,
            PS6000_ETS_MODE  mode,
            int16_t          etsCycles,
            int16_t          etsInterleave,
            int32_t         *sampleTimePicoseconds
        ); """
    make_symbol(ldlib, "SetEts", "ps6000SetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p])

    """ PICO_STATUS ps6000SetTriggerChannelProperties
        (
            int16_t                            handle,
            PS6000_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
            int16_t                            nChannelProperties,
            int16_t                            auxOutputEnable,
            int32_t                            autoTriggerMilliseconds
        ); """
    make_symbol(ldlib, "SetTriggerChannelProperties", "ps6000SetTriggerChannelProperties", c_uint32,
                [c_int16, c_void_p, c_int16, c_int16, c_int32])

    """ PICO_STATUS ps6000SetTriggerChannelConditions
        (
            int16_t                    handle,
            PS6000_TRIGGER_CONDITIONS *conditions,
            int16_t                    nConditions
        ); """
    make_symbol(ldlib, "SetTriggerChannelConditions", "ps6000SetTriggerChannelConditions", c_uint32,
                [c_int16, c_void_p, c_int16])

    """ PICO_STATUS ps6000SetTriggerChannelDirections
        (
            int16_t                       handle,
            PS6000_THRESHOLD_DIRECTION  channelA,
            PS6000_THRESHOLD_DIRECTION  channelB,
            PS6000_THRESHOLD_DIRECTION  channelC,
            PS6000_THRESHOLD_DIRECTION  channelD,
            PS6000_THRESHOLD_DIRECTION  ext,
            PS6000_THRESHOLD_DIRECTION  aux
        ); """
    make_symbol(ldlib, "SetTriggerChannelDirections", "ps6000SetTriggerChannelDirections", c_uint32,
                [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32])

    """ PICO_STATUS ps6000SetTriggerDelay
        (
            int16_t   handle,
            uint32_t  delay
        ); """
    make_symbol(ldlib, "SetTriggerDelay", "ps6000SetTriggerDelay", c_uint32, [c_int16, c_uint32])

    """ PICO_STATUS ps6000SetPulseWidthQualifier
        (
            int16_t                     handle,
            PS6000_PWQ_CONDITIONS      *conditions,
            int16_t                     nConditions,
            PS6000_THRESHOLD_DIRECTION  direction,
            uint32_t                    lower,
            uint32_t                    upper,
            PS6000_PULSE_WIDTH_TYPE     type
        ); """
    make_symbol(ldlib, "SetPulseWidthQualifier", "ps6000SetPulseWidthQualifier", c_uint32,
                [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32])

    """ PICO_STATUS ps6000IsTriggerOrPulseWidthQualifierEnabled
        (
            int16_t  handle,
            int16_t *triggerEnabled,
            int16_t *pulseWidthQualifierEnabled
        ); """
    make_symbol(ldlib, "IsTriggerOrPulseWidthQualifierEnabled", "ps6000IsTriggerOrPulseWidthQualifierEnabled", c_uint32,
                [c_int16, c_void_p, c_void_p])

    """ PICO_STATUS ps6000GetTriggerTimeOffset
        (
            int16_t            handle,
            uint32_t          *timeUpper,
            uint32_t          *timeLower,
            PS6000_TIME_UNITS *timeUnits,
            uint32_t           segmentIndex
        ); """

    """ PICO_STATUS ps6000GetTriggerTimeOffset64
        (
            int16_t              handle,
            int64_t           *time,
            PS6000_TIME_UNITS *timeUnits,
            uint32_t      segmentIndex
        ); """
    make_symbol(ldlib, "GetTriggerTimeOffset", "ps6000GetTriggerTimeOffset64", c_uint32,
                [c_int16, c_void_p, c_void_p, c_uint32])

    """ PICO_STATUS ps6000GetValuesTriggerTimeOffsetBulk
        (
            int16_t            handle,
            uint32_t          *timesUpper,
            uint32_t          *timesLower,
            PS6000_TIME_UNITS *timeUnits,
            uint32_t           fromSegmentIndex,
            uint32_t           toSegmentIndex
        ); """

    """ PICO_STATUS ps6000GetValuesTriggerTimeOffsetBulk64
        (
            int16_t            handle,
            int64_t           *times,
            PS6000_TIME_UNITS *timeUnits,
            uint32_t           fromSegmentIndex,
            uint32_t           toSegmentIndex
        );  """
    make_symbol(ldlib, "GetValuesTriggerTimeOffsetBulk", "ps6000GetValuesTriggerTimeOffsetBulk64", c_uint32,
                [c_int16, c_void_p, c_void_p, c_uint32, c_uint32])

    """ PICO_STATUS ps6000SetDataBuffers
        (
            int16_t            handle,
            PS6000_CHANNEL     channel,
            int16_t           *bufferMax,
            int16_t           *bufferMin,
            uint32_t           bufferLth,
            PS6000_RATIO_MODE  downSampleRatioMode
        ); """
    make_symbol(ldlib, "SetDataBuffers", "ps6000SetDataBuffers", c_uint32,
                [c_int16, c_int32, c_void_p, c_void_p, c_uint32, c_int32])

    """ PICO_STATUS ps6000SetDataBuffer
        (
            int16_t            handle,
            PS6000_CHANNEL     channel,
            int16_t           *buffer,
            uint32_t           bufferLth,
            PS6000_RATIO_MODE  downSampleRatioMode
        ); """
    make_symbol(ldlib, "SetDataBuffer", "ps6000SetDataBuffer", c_uint32, [c_int16, c_int32, c_void_p, c_uint32, c_int32])

    """ PICO_STATUS PREF2 PREF3 (ps6000SetDataBufferBulk)
        (
            int16_t            handle,
            PS6000_CHANNEL     channel,
            int16_t           *buffer,
            uint32_t           bufferLth,
            uint32_t           waveform,
            PS6000_RATIO_MODE  downSampleRatioMode
        ); """
    make_symbol(ldlib, "SetDataBufferBulk", "ps6000SetDataBufferBulk", c_uint32,
                [c_int16, c_int32, c_void_p, c_uint32, c_uint32, c_int32])

    """ PICO_STATUS ps6000SetDataBuffersBulk
        (
            int16_t            handle,
            PS6000_CHANNEL     channel,
            int16_t           *bufferMax,
            int16_t           *bufferMin,
            uint32_t           bufferLth,
            uint32_t           waveform,
            PS6000_RATIO_MODE  downSampleRatioMode
        ); """
    make_symbol(ldlib, "SetDataBuffersBulk", "ps6000SetDataBuffersBulk", c_uint32,
                [c_int16, c_int32, c_void_p, c_void_p, c_uint32, c_uint32, c_int32])

    """ PICO_STATUS ps6000SetEtsTimeBuffer
        (
            int16_t   handle,
            int64_t  *buffer,
            uint32_t  bufferLth
        ); """
    make_symbol(ldlib, "SetEtsTimeBuffer", "ps6000SetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_uint32])

    """ PICO_STATUS ps6000SetEtsTimeBuffers
        (
            int16_t   handle,
            uint32_t *timeUpper,
            uint32_t *timeLower,
            uint32_t  bufferLth
        ); """

    """ PICO_STATUS ps6000RunBlock
        (
            int16_t           handle,
            uint32_t          noOfPreTriggerSamples,
            uint32_t          noOfPostTriggerSamples,
            uint32_t          timebase,
            int16_t           oversample,
            int32_t          *timeIndisposedMs,
            uint32_t          segmentIndex,
            ps6000BlockReady  lpReady,
            void             *pParameter
        ); """
    make_symbol(ldlib, "RunBlock", "ps6000RunBlock", c_uint32,
                [c_int16, c_uint32, c_uint32, c_uint32, c_int16, c_void_p, c_uint32, c_void_p, c_void_p])

    """ PICO_STATUS ps6000IsReady
        (
            int16_t  handle,
            int16_t *ready
        ); """
    make_symbol(ldlib, "IsReady", "ps6000IsReady", c_uint32, [c_int16, c_void_p])

    """ PICO_STATUS ps6000RunStreaming
        (
            int16_t            handle,
            uint32_t          *sampleInterval,
            PS6000_TIME_UNITS  sampleIntervalTimeUnits,
            uint32_t           maxPreTriggerSamples,
            uint32_t           maxPostPreTriggerSamples,
            int16_t            autoStop,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           overviewBufferSize
        ); """
    make_symbol(ldlib, "RunStreaming", "ps6000RunStreaming", c_uint32,
                [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32])

    """ PICO_STATUS ps6000GetStreamingLatestValues
        (
            int16_t               handle,
            ps6000StreamingReady  lpPs6000Ready,
            void                 *pParameter
        ); """
    make_symbol(ldlib, "GetStreamingLatestValues", "ps6000GetStreamingLatestValues", c_uint32,
                [c_int16, c_void_p, c_void_p])

    """ PICO_STATUS ps6000NoOfStreamingValues
        (
            int16_t   handle,
            uint32_t *noOfValues
        ); """
    make_symbol(ldlib, "NoOfStreamingValues", "ps6000NoOfStreamingValues", c_uint32, [c_int16, c_void_p])

    """ PICO_STATUS ps6000GetMaxDownSampleRatio
        (
            int16_t            handle,
            uint32_t           noOfUnaggreatedSamples,
            uint32_t          *maxDownSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           segmentIndex
        ); """
    make_symbol(ldlib, "GetMaxDownSampleRatio", "ps6000GetMaxDownSampleRatio", c_uint32,
                [c_int16, c_uint32, c_void_p, c_int32, c_uint32])

    """ PICO_STATUS ps6000GetValues
        (
            int16_t            handle,
            uint32_t           startIndex,
            uint32_t          *noOfSamples,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           segmentIndex,
            int16_t           *overflow
        ); """
    make_symbol(ldlib, "GetValues", "ps6000GetValues", c_uint32,
                [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

    """ PICO_STATUS ps6000GetValuesBulk
        (
            int16_t            handle,
            uint32_t          *noOfSamples,
            uint32_t           fromSegmentIndex,
            uint32_t           toSegmentIndex,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            int16_t           *overflow
        ); """
    make_symbol(ldlib, "GetValuesBulk", "ps6000GetValuesBulk", c_uint32,
                [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p])

    """ PICO_STATUS ps6000GetValuesAsync
        (
            int16_t            handle,
            uint32_t           startIndex,
            uint32_t           noOfSamples,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           segmentIndex,
            void              *lpDataReady,
            void              *pParameter
        ); """
    make_symbol(ldlib, "GetValuesAsync", "ps6000GetValuesAsync", c_uint32,
                [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p])

    """ PICO_STATUS ps6000GetValuesOverlapped
        (
            int16_t            handle,
            uint32_t           startIndex,
            uint32_t          *noOfSamples,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           segmentIndex,
            int16_t           *overflow
        ); """
    make_symbol(ldlib, "GetValuesOverlapped", "ps6000GetValuesOverlapped", c_uint32,
                [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

    """ PICO_STATUS ps6000GetValuesOverlappedBulk
        (
            int16_t            handle,
            uint32_t           startIndex,
            uint32_t          *noOfSamples,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           fromSegmentIndex,
            uint32_t           toSegmentIndex,
            int16_t           *overflow
        ); """
    make_symbol(ldlib, "GetValuesOverlappedBulk", "ps6000GetValuesOverlappedBulk", c_uint32,
                [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_uint32, c_void_p])

    """ PICO_STATUS ps6000GetValuesBulkAsyc
        (
            int16_t            handle,
            uint32_t           startIndex,
            uint32_t          *noOfSamples,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           fromSegmentIndex,
            uint32_t           toSegmentIndex,
            int16_t           *overflow
        ); """

    """ PICO_STATUS ps6000GetNoOfCaptures
        (
            int16_t   handle,
            uint32_t *nCaptures
        ); """
    make_symbol(ldlib, "GetNoOfCaptures", "ps6000GetNoOfCaptures", c_uint32, [c_int16, c_void_p])

    """ PICO_STATUS ps6000GetNoOfProcessedCaptures
        (
            int16_t   handle,
            uint32_t *nProcessedCaptures
        ); """
    make_symbol(ldlib, "GetNoOfProcessedCaptures", "ps6000GetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p])

    """ PICO_STATUS ps6000Stop
        (
            int16_t  handle
        ); """
    make_symbol(ldlib, "Stop", "ps6000Stop", c_uint32, [c_int16, ])

    """ PICO_STATUS ps6000SetNoOfCaptures
        (
            int16_t   handle,
            uint32_t  nCaptures
        ); """
    make_symbol(ldlib, "SetNoOfCaptures", "ps6000SetNoOfCaptures", c_uint32, [c_int16, c_uint32])

    """ PICO_STATUS ps6000SetWaveformLimiter
        (
            int16_t   handle,
            uint32_t  nWaveformsPerSecond
        ); """
    make_symbol(ldlib, "SetWaveformLimiter", "ps6000SetWaveformLimiter", c_uint32, [c_int16, c_uint32])


    """ PICO_STATUS ps6000SetExternalClock
        (
            int16_t                    handle,
            PS6000_EXTERNAL_FREQUENCY  frequency,
            int16_t                    threshold
        ); """
    make_symbol(ldlib, "SetExternalClock", "ps6000SetExternalClock", c_uint32, [c_int16, c_int32, c_int16])


    """ PICO_STATUS ps6000GetAnalogueOffset
        (
            int16_t          handle,
            PS6000_RANGE     range,
            PS6000_COUPLING  coupling,
            float           *maximumVoltage,
            float           *minimumVoltage
        ); """
    make_symbol(ldlib, "GetAnalogueOffset", "ps6000GetAnalogueOffset", c_uint32,
                [c_int16, c_int32, c_int32, c_void_p, c_void_p])
'''