import pwint
pp = pwint.pwint

_inspect_lookup = {}  # keys object class to switch cases for inspect()
_state = {
    "debug": False
}

def inspect(o, *args, **kwargs):
    obj_class = type(o).__name__
    _func = _inspect_lookup[obj_class]
    _func(o)

def _switch_e(e, *args, **kwargs):
    #print("switch e hit")
    _doc = [["Inspecting '{}'\n\tCluster attributes:".format(e.id)],{"indent":1}, {"debug":False, "indent":2, "columns":8, "column_width":12 }]
    _attribute_list = []
    for key in e.components:
        for i in e.components.get(key).__dict__:
            if i not in _common_variables_blacklist:
                _attribute_list.append(i)
    _doc.append(_attribute_list)
    print("\n####", _doc)
    pp(_doc)
    return e

def _switch_c(c, *args, **kwargs):
    print("\tswitch c")

    return []


def _switch_s(s, *args, **kwargs):
    print("\tswitch s")

    return []


def _switch_r(r, *args, **kwargs):
    print("\tswitch r")

    return []

_inspect_lookup.update({
    "Entity": _switch_e,
    "Component": _switch_c,
    "System": _switch_s,
    "Rack": _switch_r})

_common_variables_blacklist = ["id", "key", "purge", "entity"]




