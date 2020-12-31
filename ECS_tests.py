import ECS
import ECS_tools as tools
import random
import string
import pwint


def divider_function(msg):
    _deco = "~~"
    print("{}{:-^70}{}".format(_deco, msg, _deco))


def populate_manipulate(r, e_spawn=500, k_spawn=40):
    divider_function("Beginning test 'populate_manipulate'")

    my_entities = []
    component_keys = []
    for i in range(e_spawn):
        my_entities.append(r.register(ECS.Entity()))

    for i in range(k_spawn):
        component_keys.append(
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=(random.randint(5, 10)))))

    for i in my_entities:
        i.grant(r.register(ECS.Component("dummy")))
        components_to_install = random.randint(20, 30)
        done_selecting = False
        while not done_selecting:
            c_to_add = component_keys[random.randint(1, len(component_keys) - 1)]
            if c_to_add not in i.components:
                i.grant(r.register(ECS.Component(c_to_add)))
                components_to_install -= 1
                if components_to_install <= 0:
                    done_selecting = True
        # print("{} granted {} components".format(i.id, len(i.components)))
    print(r)

    def murderbot():
        rand_num_in_range = random.randint(0, len(r.entities) - 1)
        racked_entities = list(r.entities.keys())
        r.purge(r.entities[racked_entities[rand_num_in_range]])

    function_profile = (murderbot, divider_function)
    s = r.register(ECS.System(("dummy",), (function_profile), "murderbot"))

    def inspect_random_entity():
        rand_num_in_range = random.randint(0, len(r.entities) - 1)
        racked_entities = list(r.entities.keys())

        # TODO: disabling for inspect rewrite
        # tools.inspect_entity(r.entities[racked_entities[rand_num_in_range]])

    inspect_random_entity()
    inspect_random_entity()
    inspect_random_entity()

    # while len(r.entities) > 0:
    # s.update()
    print(r)
    divider_function("Ending test 'populate_manipulate'")
    return r


def blueprinting(r):
    divider_function("Beginning test 'blueprinting'")

    def spawn_one():
        e = r.register(ECS.Entity())
        c = r.register(ECS.Component("position"))
        c.x = 3
        e.grant(c)

        return e

    e = spawn_one()
    # TODO: disabling for inspect rewrite
    # tools.inspect_entity(e)
    print("\t Entity is at X: {} Y:{}".format(e.components["position"].x, e.components["position"].y))

    e_2 = spawn_one()
    e_2.grant(r.register(ECS.Component("color")))
    # TODO: disabling for inspect rewrite
    # tools.inspect_entity(e_2)
    print("\nColour 'Hot'\n\tRED:\t{}\n\tGREEN:\t{}\n\tBLUE:\t{}".format(
        e_2.components["color"].colors["hot"][0],
        e_2.components["color"].colors["hot"][1],
        e_2.components["color"].colors["hot"][2]))
    divider_function("Ending test 'blueprinting'")
    return r


def inspecting(r):
    divider_function("Starting test 'inspecting'")
    e = r.register(ECS.Entity())
    c = r.register(ECS.Component("color"))
    e.grant(c)
    e.grant(r.register(ECS.Component("position")))

    # tools.inspect_rack(r)

    # for id_key in r.components["dummy"]:
    # tools.inspect_entity(r.components["dummy"].get(id_key).entity)

    # tools.inspect_rack(r)
    tools.inspect(e)

    component_keys = []
    for i in range(23):
        component_keys.append(
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=(random.randint(4, 10)))))

    for key in component_keys:
        e.grant(r.register(ECS.Component(key)))

    tools.inspect(e)

    divider_function("Ending test 'inspecting'")
    return r


def custom_print(r):
    divider_function("Starting test 'pp'")
    long_test_series = [
        ["Heading A"],
        {"indent": 1, "column_width": 20, "columns": 2, "filler": "."},
        ["sandwich", "7.99", "fries", "3.99", "hort dorg", "6.20", "borgar", "9.99"],

        ["Sub-Heading A"],
        {"indent": 1, "columns":1 },
        ["This menu posted by borgar gang", "this is like a paragraph i guess", "haha"],

        {"indent": 0},
        ["Heading B"],
        {"indent" :1, "column_width": 20, "columns": 3, "filler": ""},
        ["DAY", "OPEN", "CLOSED"],
        {"filler": "."},
        ["mon", "8am", "10pm",
         "tue", "8am", "8pm",
         "wed", "8am", "10pm",
         "thur", "8am", "10pm",
         "fri", "8am", "10pm",
         "sat", "8am", "10pm",
         "sun", "CLOSED"]]

    test_series = [
    ["Heading A"],
    {"indent": 1, "column_width": 30, "columns": 2},
    ["sandwich", "7.99", "fries", "3.99", "hort dorg", "6.20", "borgar", "9.99"],
    ]

    pwint.pwint(test_series, 10, "trash", ("nonsense", "more nonsense"), debug=True, bad_keyword = "garbage")

    pwint.pwint(long_test_series, debug=True)

    divider_function("Ending test 'pp'")
    return r
