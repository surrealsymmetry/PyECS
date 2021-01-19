state = {  # considered just shoving state into kwargs but idk how id set defaults
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

default_state = state.copy()

# todo make asserts that give pwinty very clear feedback if poorly formed list/dict passed

def pwint(series, **kwargs):
    ### items in the series are either lists of strings k:v entries
    ### a k:v entry updates the default values (default values reset for each )
    for key in kwargs:
        if key in state:
            state.update({key: kwargs[key]})
        else:
            if state["debug"]:
                print("|'{0}' is an unknown kwarg, ignoring '{0}'".format(key))
    if "preserve" not in kwargs:
        state.update(default_state.copy())

    def indents():
        # if state["debug"]:
        # print("| indents(): {}".format(state["indent"]))
        return "{:\t<{}}".format("", state["indent"])

    for i in series:
        if type(i) is dict:
            flag_changes = ""
            for key in i:
                if key == "indent":  # is it indent state information?
                    increment_value = i[key]

                    if increment_value == 0:
                        state["indent"] = 0
                    else:
                        state["indent"] += i[key]

                else:  # its not indent information  so we'll update state
                    if state[key] != i[key]:
                        flag_changes += "\n\t| '{}' '{}' (was '{}'), ".format(key, i[key], state[key])

                    state.update({key: i[key]})

            if state["debug"]:
                if len(flag_changes) > 0:
                    flag_changes = "| FLAG CHANGES:" + flag_changes
                    print(flag_changes)


        elif type(i) is list:
            for j in range(len(i)):
                i[j] = str(i[j])
            for j in range(len(i)):
                assert type(i[j]) is str, "Something in a list resisted the string lifestyle"

            column_counter = 0
            # initialize the block at the right indent level
            doc = indents()
            final_width = state["column_width"]
            border_width = 2

            if type(state["key"]) is int: # if the default is present instead of a custom lambda sort
                sorted_list = i.copy()  # must be a copy! making this a reference to the original list is destructive!
            else:
                sorted_list = sorted(i, key=state["key"], reverse=state["reverse"])
            # stripping newlines in columned items

            for index_of_string in range(len(sorted_list)):
                swap = {"\n": " ", "\t": " "}  # blacklisted characters replacement values
                current_string = sorted_list[index_of_string]
                done = False
                # strip illegal characters UNLESS its a single item heading or a single column list

                if len(sorted_list) > 1 or state["indent"] > 0:
                    while not done:
                        if len(current_string)>0:
                            for index_of_char in range(len(current_string)):  # per character
                                _char = current_string[index_of_char]

                                if _char in swap:
                                    leading_split = current_string[0: index_of_char]
                                    trailing_split = current_string[index_of_char + 1: len(current_string)]
                                    current_string = "{}{}{}".format(leading_split, swap[_char], trailing_split)
                                    sorted_list[index_of_string] = current_string

                                elif index_of_char >= len(current_string) - 1:
                                    done = True

                # either clip the strings or track max
                if len(current_string) >= state["column_width"]:
                    if state["force_width"]:
                        current_string = current_string[0:final_width]
                        sorted_list[index_of_string] = current_string
                    else:
                        if len(current_string) > final_width:
                            final_width = len(current_string)

            last_position = 0

            for current_string in sorted_list:
                if 0 < column_counter < state["columns"]:  # if current position is between a first and last columns
                    filler_to_add = final_width - last_position
                    filler = "{:{}<{}}".format("", state["filler"], filler_to_add + border_width)
                    doc += filler
                if column_counter >= state["columns"]:
                    doc += "\n{}".format(indents())
                    column_counter = 0

                doc += "{}".format(current_string)
                last_position = len(current_string)
                column_counter += 1
            print(doc)

        else:
            if state["debug"]:
                print("Unknown type {} passed to pwint, ".format(type(i).__name__))
