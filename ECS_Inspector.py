import pwint
pp = pwint.pwint

inspect_lookup = {}  # keys object class to switch cases for inspect()
state = {
    "debug": False
}

def inspect(o):
    obj_class = type(o).__name__
    _func = inspect_lookup[obj_class]
    _func(o)

def _switch_e(e):
    #print("switch e hit")
    doc = [["\nInspecting '{}'\n\tCluster attributes:".format(e.id)],{"indent":1}, {"indent":2, "force_width":True, "columns":2, "column_width":30, "filler":"." }]

    for key in e.components:
        common_attributes_blacklist = {"key":None, "id":None, "purge":None, "entity":None}
        attribute_list = []

        for attribute in e.components.get(key).__dict__:
            # attribute_value_type = type(getattr(e.components[key], attribute)).__name__
            # print(attribute_value_type)

            if attribute in common_attributes_blacklist:
                common_attributes_blacklist.update({ attribute : str(getattr(e.components[key], attribute))})
            else:
                attribute_list.append("{}".format(attribute))
                attribute_list.append(str(getattr(e.components[key], attribute)))

        doc.append(["Aspect: '{}'".format(key)])
        doc.append({"indent":1})
        doc.append(["ID: {}".format(common_attributes_blacklist["id"])])
        doc.append(attribute_list)
        doc.append({"indent": -1})


    pp(doc)
    return e

def _switch_c(c):
    common_attributes_blacklist = {"key": None, "id": None, "purge": None, "entity": None}
    attribute_list = []
    for attribute in c.__dict__:
        if attribute in common_attributes_blacklist:
            common_attributes_blacklist.update({attribute: str(getattr(c, attribute))})
        else:
            attribute_list.append("{}".format(attribute))
            attribute_list.append(str(getattr(c, attribute)))
    cluster_list = []
    for key in c.entity.components:
        cluster_list.append("'{}'".format(key))

    doc = [] # is this nicer than the repeated doc.append()s seen above? probably
    doc += [
        ["\nInspecting '{}'".format(c.id)], {"indent": 1},
        ["Cluster of entity {}".format(c.entity.id)],
        {"indent":1, "columns":5, "column_width":15, "force_width":False, "filler":" "},
            cluster_list,
        {"indent":-1}, ["Attributes of {}".format(c.id)],
        {"indent": 1, "force_width": True, "columns": 2, "column_width": 30, "filler": "."},
            attribute_list]
    pp(doc)

    return []


def _switch_s(s):
    print("\tswitch s")

    return []


def _switch_r(r, *args, **kwargs):
    print("\tswitch r")

    return []

inspect_lookup.update({
    "Entity": _switch_e,
    "Component": _switch_c,
    "System": _switch_s,
    "Rack": _switch_r})





