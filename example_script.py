'''
This is an example script showing some basic use cases of popular instruments.
An instrument needs to be connected.
'''


''''''''''''''''''''''''''''''''''''''''''''''''
'''			Import and Initialization		 '''
''''''''''''''''''''''''''''''''''''''''''''''''
import pyauto

b = pyauto.Bench()



''''''''''''''''''''''''''''''''''''''''''''''''
'''		Scanning Bench and Query IDN		 '''
''''''''''''''''''''''''''''''''''''''''''''''''
b.scan_bench()

p0 = b.power_supply[0]

p0_id = p0.comm('*IDN?')



''''''''''''''''''''''''''''''''''''''''''''''''
'''	Using Basic power_supply Functions		 '''
''''''''''''''''''''''''''''''''''''''''''''''''
p0.set_voltage(3.3)
p0.set_current(1)

p0.set_out_state(1)

current = p0.meas_current()



''''''''''''''''''''''''''''''''''''''''''''''''
'''				Iterate Through Bench		 '''
''''''''''''''''''''''''''''''''''''''''''''''''
for inst in b:
	if inst.type == 'power_supply':
		print(inst.id)



''''''''''''''''''''''''''''''''''''''''''''''''
'''	Using Basic power_supply Functions		 '''
''''''''''''''''''''''''''''''''''''''''''''''''
class myTestPlan(pyauto.TestPlan):
	def test_001(self):

