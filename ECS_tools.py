
def inspect_entity(e):
    print("\nInspecting", e)
    msg = ""
    for key in e.components:
        msg += "\t{}".format(inspect_component(e.components[key]))
    print(msg)

def inspect_component(c):
    assert type(c).__name__ == "Component"
    msg = ""
    _default_variables_blacklist = ["key", "id", "purge", "entity"]
    for i in c.__dict__:
        if i not in _default_variables_blacklist:
            msg = "{}{}".format(msg, i)
    print(msg)

def inspect_rack(r):
    print("\nInspecting Rack", r)
    msg = ""
    for key in r.components:
        msg = "{}\n\t{:>10}{:>5}".format(msg, key, len(r.components[key]))
    print(msg)

