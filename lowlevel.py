import re

def instantiate_inst(inst_id, inst, connection_mode, unknown):
    '''creates instrument and passes it back as a list'''
    if unknown:
        gid = 'unknown'
    else:
        gid = inst_id
        
    exec(f'from cInst_{gid} import cInst_{gid}')

    if connection_mode == "USB":
        inst_str = str(inst).split("::")
        if len(inst_str) > 1:
            address = inst_str[-2]
        else:
            address = inst_str[0]
    else:
        address = str(inst).split("::")[1]

    inst_to_add = eval(f'cInst_{gid}(inst, inst_id, connection_mode, address)') #this will return either a single object or a list of multiple objects
    if type(inst_to_add) is list:
        return inst_to_add
    else:
        return [inst_to_add]
