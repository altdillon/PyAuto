import re

def instantiate_inst(class_name, inst):
	'''creates instrument and passes it back as a list'''
	eval(f'from {class_name} import {class_name}')

	connection_mode = re.sub(r'\d+','',str(inst))[:5].strip("In")
	if connection_mode == "USB":
		address = (str(inst).split("::")[-2])
	else:
		address = (str(inst).split("::")[1])
        
	inst_to_add = eval(f'{class_name}(temp, class_name[6:], connection_mode, address)') #this will return either a single object or a list of multiple objects
	if type(inst_to_add) is list:
		return inst_to_add
	else:
		return [inst_to_add]