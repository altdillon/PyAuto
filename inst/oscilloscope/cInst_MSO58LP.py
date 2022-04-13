from cInst_oscilloscope import cInst_oscilloscope
import time

class cInst_MSO58LP(cInst_oscilloscope):
    '''
    TBD
    '''
    def set_measurement(self, ...):
        '''
        See page 500 ish in the 5 series manual
        '''
        
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

        with open(filename,'w') as fp:
            fp.write(raw)
