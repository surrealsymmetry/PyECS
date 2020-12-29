def inspect_entity(e):
    msg = ""
    for key in e.components:
        msg += inspect_component(e.components[key])
    print(e, msg)

def inspect_component(c):
    att_list = []
    for i in c.__dict__:
        att_list.append(i)
    return str(att_list)