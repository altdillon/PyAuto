'''
This is an example script showing some basic use cases of popular instruments.
'''

import pyauto

b = pyauto.scan_bench()

PowSup = b.power_supply[0]

PowSup.set_voltage(3.3)
PowSup.set_current(1)

PowSup.set_out_state(1)

print(PowSup.meas_current())


''' To be implemented later
for inst in b:
	if inst.type == 'power_supply'

'''