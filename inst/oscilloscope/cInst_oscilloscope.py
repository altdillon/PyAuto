from cInst import cInst
import time

class cInst_oscilloscope(cInst):
    '''
    oscilloscope main class
    '''

    def autoset(self):
        """Performs front panel equivalent of AUTOSET"""
        self.comm("AUTOS EXEC")

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

    def set_time_base(self,timebase = 0.000000001):
        '''
        sets horizontal scale (seconds/division)
        '''
        self.comm('HORIZONTAL:SCA {}'.format(timebase))

    def get_time_base(self):
        """
        Returns the time base(second per division)
        """
        return float(self.comm("HOR:SCA?"))

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

    def set_sampling_rate(self,rate = 20e9):
        """
        Set the sampling rate of the scope. Based on the time axis duration, the value set may be adjusted automatically by the scope
        rate = sampling rate in samples/second
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