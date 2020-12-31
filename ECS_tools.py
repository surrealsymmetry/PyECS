_inspect_lookup = {}  # keys object class to switch cases for inspect()


def inspect(o, *args, **kwargs):
    def _switch_e(e, *args, **kwargs):

        # print("\tswitch e")
        set = [[e.id, 1]]
        key_list = []
        for key in e.components:
            key_list.append(key)
        set.append(key_list)

        return set

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

    obj_class = type(o).__name__
    _func = _inspect_lookup[obj_class]
    print("\nInspecting {}".format(obj_class))



