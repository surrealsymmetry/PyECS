def pwint(series, *args, **kwargs):
    ### items in the series are either lists of strings k:v entries
    ### a k:v entry updates the default values (default values reset for each )
    _state = {  # considered just shoving state into kwargs but idk how id set defaults
        "columns": 3,
        "column_width": 18,
        "indent": 0,
        "debug": False,
        "filler": " "
    }

    for key in kwargs:
        if key in _state:
            _state.update({key: kwargs[key]})
            if _state["debug"]:
                print("Flag '{}' set to {}".format(key, _state[key]))
        else:
            if _state["debug"]:
                print("'{0}' is not , ignoring '{0}'".format(key))

    for arg in args:
        if _state["debug"]:
            print("ignoring argument {}".format(arg))

    def indents():
        return "{:\t<{}}".format("", _state["indent"])

    for i in series:
        if type(i) is dict:
            # everything from here to the update is just for debug printing
            _flag_changes = "Flag changes:"
            for key in i:
                _old_value = _state[key]
                _new_value = i[key]

                if key == "indent":             # if the dict value being passed by the series
                    if i[key] == 0:
                        _state["indent"] = 0
                    else:
                        if _state["debug"]:
                            print("Modifying indents by {}".format(i[key]))
                        _state["indent"] += i[key]
                else:
                    if _old_value != _new_value:
                        _flag_changes += "\n\t'{}' '{}' (was '{}'), ".format(key, _new_value, _old_value)
            if _state["debug"]:
                print(_flag_changes)  # after all keys checked, print the changes

            _state.update(i)

        elif type(i) is list:
            _column_counter = 0

            # initialize the block at the right indent level
            _msg = indents()

            # this refers to the padding still required from the previous loop
            # padding is added right before the next element
            _pad_to_reach_target_width = 0
            for j in i:

                if _column_counter >= _state["columns"]:
                    _msg += "\n{}".format(indents())
                    _column_counter = 0

                if _column_counter != 0: #if not at start of a line, add pad
                    if _state["debug"]:
                        print("\tDEBUG: {}: {} minus {} equals {}".format(j, _state["column_width"], len(j), _pad_to_reach_target_width))
                    _msg += "{:{}<{}}".format("", _state["filler"], _pad_to_reach_target_width)
                _msg += "{}".format(j)
                _pad_to_reach_target_width = _state["column_width"] - len(j)
                _column_counter += 1
            print(_msg)

        else:
            if _state["debug"]:
                print("Unknown type {} passed to pwint, ".format(i))
