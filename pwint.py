def pwint(series, *args, **kwargs):
    print("\n")
    ### items in the series are either lists of strings k:v entries
    ### a k:v entry updates the default values (default values reset for each )

    _state = {  # considered just shoving _state into kwargs but idk how id set defaults
        "columns": 4,
        "column_width": 10,
        "indent": 0,  # this value is accessed indirectly, providing indent keys increments position or resets if zero
        "debug": False,
        "filler": " ",
        "force_width": False,

        # kwargs for sort(), again this is removable if kwargs is just queried directly but i like the default values per call
        "key": 0,  # a function which is passed to sort(key= function )
        "reverse": False
    }

    for key in kwargs:
        if key in _state:
            _state.update({key: kwargs[key]})
        else:
            if _state["debug"]:
                print("|'{0}' is an unknown kwarg, ignoring '{0}'".format(key))

    for arg in args:
        if _state["debug"]:
            print("| ignoring argument {}".format(arg))

    def indents():
        # if _state["debug"]:
        # print("| indents(): {}".format(_state["indent"]))
        return "{:\t<{}}".format("", _state["indent"])

    for i in series:
        if type(i) is dict:
            _flag_changes = ""
            for key in i:
                if key == "indent":  # is it indent state information?
                    increment_value = i[key]

                    if increment_value == 0:
                        _state["indent"] = 0
                    else:
                        _state["indent"] += i[key]

                else:  # its not indent information  so we'll update state
                    if _state[key] != i[key]:
                        _flag_changes += "\n\t| '{}' '{}' (was '{}'), ".format(key, i[key], _state[key])

                    _state.update({key: i[key]})

            if _state["debug"]:
                if len(_flag_changes) > 0:
                    _flag_changes = "| FLAG CHANGES:" + _flag_changes
                    print(_flag_changes)


        elif type(i) is list:
            _column_counter = 0
            # initialize the block at the right indent level
            _doc = indents()
            _final_width = _state["column_width"]
            _border_width = 2

            if type(_state["key"]) is int:
                sorted_list = i.copy()  # must be a copy! making this a reference to the original list is destructive!
            else:
                sorted_list = sorted(i, key=_state["key"], reverse=_state["reverse"])
            # stripping newlines in columned items

            for index_of_string in range(len(sorted_list)):
                string = sorted_list[index_of_string]
                _swap = {"\n": " ", " ": " / "}  # blacklisted characters replacement values
                _done = False
                # strip illegal characters UNLESS its a single item heading or a single column list

                if len(sorted_list) > 1 or _state["indent"] > 0:
                    while not _done:
                        for index_of_char in range(len(string)):  # per character
                            _char = string[index_of_char]
                            if _char in _swap:
                                _leading_split = string[0: index_of_char]
                                _trailing_split = string[index_of_char + 1: len(string)]

                                string = "{}{}{}".format(_leading_split, _swap[_char], _trailing_split)

                                sorted_list[index_of_string] = string
                            elif index_of_char >= len(string) - 1:
                                _done = True

                # either clip the strings or track max
                if len(string) >= _state["column_width"]:
                    if _state["force_width"]:
                        string = string[0:_final_width]
                        sorted_list[index_of_string] = string
                    else:
                        if len(string) > _final_width:
                            _final_width = len(string)

            _last_position = 0

            for string in sorted_list:
                if 0 < _column_counter < _state["columns"]:  # if current position is between a first and last columns
                    _filler_to_add = _final_width - _last_position
                    filler = "{:{}<{}}".format("", _state["filler"], _filler_to_add + _border_width)
                    _doc += filler
                if _column_counter >= _state["columns"]:
                    _doc += "\n{}".format(indents())
                    _column_counter = 0

                _doc += "{}".format(string)
                _last_position = len(string)
                _column_counter += 1
            print(_doc)

        else:
            if _state["debug"]:
                print("Unknown type {} passed to pwint, ".format(type(i).__name__))
