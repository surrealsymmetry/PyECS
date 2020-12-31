
def pwint(series, *args, **kwargs):
    ### items in the series are either lists of strings k:v entries
    ### a k:v entry updates the default values (default values reset for each )

    _state = {  # considered just shoving _state into kwargs but idk how id set defaults
        "columns": 3,
        "column_width": 18,
        "indent": 0,
        "debug": False,
        "filler": " "
    }
    for key in kwargs:
        if key in _state:
            _state.update({key: kwargs[key]})
        else:
            if _state["debug"]:
                print("|'{0}' is not , ignoring '{0}'".format(key))

    for arg in args:
        if _state["debug"]:
            print("| ignoring argument {}".format(arg))

    def indents():
        #if _state["debug"]:
            #print("| indents(): {}".format(_state["indent"]))
        return "{:\t<{}}".format("", _state["indent"])

    for i in series:
        if type(i) is dict:
            _flag_changes = ""
            for key in i:
                if key == "indent":
                    increment_value = i[key]
                    if _state["debug"]:
                        print("| 'indent' flag hit, adding {} to current indent of {}".format(increment_value, _state[key]))
                    if increment_value == 0:
                        _state["indent"] = 0
                        if _state["debug"]:
                            print("{}| Indent reset to {}".format(indents(), _state["indent"]))
                    else:
                        _state["indent"] += i[key]
                        if _state["debug"]:
                            print("{}|new indent level {}".format(indents(), _state["indent"]))
                else:
                    if _state[key] != i[key]:
                        if _state["debug"]:
                            print("| {}\told: {}\tnew: '{}'".format(key, _state[key], i[key]))
                        _flag_changes += "\n| '{}' '{}' (was '{}'), ".format(key, i[key], _state[key])

                    _state.update({key: i[key]})

            #if _state["debug"]:
            if len(_flag_changes) > 0:
                _flag_changes = "| FLAG CHANGES:" + _flag_changes
                if _state["debug"]:
                    print(_flag_changes)  # after all keys checked, print the changes

        elif type(i) is list:
            if _state["debug"]:
                print("{}| text Block printing at indent {}".format(indents(), _state["indent"]))
            _column_counter = 0

            # initialize the block at the right indent level
            _msg = indents()

            # this refers to the padding still required from the previous loop
            # padding is added right before the next element
            _pad_to_reach_target_width = 0
            for j in i:
                if _column_counter != 0 and _column_counter != _state["columns"]: #if not at start of a line, add pad
                    _msg += "{:{}<{}}".format("", _state["filler"], _pad_to_reach_target_width)

                if _column_counter >= _state["columns"]:
                    if _state["debug"]:
                        _msg += ("\t| counter hit, {} indent".format(_state["indent"]))
                    _msg += "\n{}".format(indents())

                    _column_counter = 0
                _msg += "{}".format(j)
                if _state["debug"]:
                    _msg += "({})".format(_state["indent"])
                _pad_to_reach_target_width = _state["column_width"] - len(j)
                _column_counter += 1
            print(_msg)

        else:
            if _state["debug"]:
                print("Unknown type {} passed to pwint, ".format(type(i).__name__))
