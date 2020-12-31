_inspect_lookup = {}  # keys object class to switch cases for inspect()


def inspect(o, *args, **kwargs):
    obj_class = type(o).__name__
    _func = _inspect_lookup[obj_class]
    print("\nInspecting {}".format(obj_class))

    indent_counter = 1

    for i in set:  # i is a subset
        _msg = ""
        _columns_to_display = 3
        _column_count = 0
        _column_width = 18
        for indent in range(indent_counter):
            _msg += "\t"
        for j in i:  # j is a sub-set element, it should be a string or a num
            if type(j) is str:
                if len(j) < _column_width:
                    _padding = _column_width - len(j)
                    _msg += "{}{:<{}}".format(j, "", _padding)

                _column_count += 1
                if _column_count >= _columns_to_display:
                    _msg += "\n"
                    for indent in range(indent_counter):
                        _msg += "\t"
                    _column_count = 0
            elif type(j) is int:
                indent_counter += j
                # print("num {} hit, new indent_counter value {}".format(j, indent_counter))

        print(_msg)  # end each list by removing hanging comma


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
