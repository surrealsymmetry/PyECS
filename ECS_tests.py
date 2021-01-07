import ECS
import ECS_Inspector as tools
import random
import string
import pwint
pp = pwint.pwint


def divider_function(msg):
    _deco = "~~"
    print("{}{:-^70}{}".format(_deco, msg, _deco))


def populate_manipulate(r, e_spawn=500, k_spawn=40):
    divider_function("Beginning test 'populate_manipulate'")

    my_entities = []
    component_keys = []
    for i in range(e_spawn):
        my_entities.append(ECS.Entity(r))

    for i in range(k_spawn):
        component_keys.append(
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=(random.randint(5, 10)))))

    for i in my_entities:
        i.grant((ECS.Component(r, "dummy")))
        components_to_install = random.randint(20, 30)
        done_selecting = False
        while not done_selecting:
            c_to_add = component_keys[random.randint(1, len(component_keys) - 1)]
            if c_to_add not in i.components:
                i.grant(ECS.Component(r, c_to_add))
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


def printing_and_sorting(r):
    divider_function("Starting test 'printing and sorting'")
    f_nam = ["becky", "noah", "bri","jasper", "colin", "sandra", "peppin", "eleanor", "chester", "angelina", "grint", "oswald", "fiona", "parker", "trisha", "joanne", "serena"]
    l_nam = ["dreck", "berd", "auren", "suarez", "peach", "duard", "nona", "poleck","merino", "grant", "chi", "decker", "wolf", "khan", "smith", "durent", "blunt", "parcey" ]
    for i in range(len(f_nam)):
        for j in range(len(l_nam)):
            c = ECS.Component(r, "name") #doc=[["Component Spawning:"]])
            c.name = "{} {}".format(f_nam[i], l_nam[j])
            e = ECS.Entity(r) #doc=[["Entity Spawning:"]])
            e.grant(c)
            # print("{}\t{} {}".format(e.id, e.components["name"].name[0], e.components["name"].name[1]))

    print("{} entities spawned".format(len(r.entities)))

    list = []
    for key in r.entities:
        e = r.entities[key]
        name = e.components["name"].name
        list.append("{} : {}".format(e.id, name))

    pp([["Unsorted"], {"columns": 4, "column_width":20, "indent":1}, list])
    pp([["Last Name Sort"], {"columns": 4, "column_width":20, "indent":1,
                "key":lambda x: x.split(" ")[3]},list])
    pp([["Reverse First Name Sort"], {"columns": 4, "column_width": 20, "indent": 1,
                "key": lambda x: x.split(" ")[2], "reverse":True}, list])
    pp([["Name Length Sort"], {"columns": 4, "column_width": 20, "indent": 1,
                "key": lambda x: len(x.split(" ")[2] + x.split(" ")[3])}, list])

    _trash_list = []
    for i in range(20):
        _piece_of_trash = ''.join(random.choices(string.ascii_uppercase + string.digits, k=(random.randint(3, 10))))
        _trash_list.append(_piece_of_trash)
        _piece_of_trash = ''.join(random.choices(string.ascii_uppercase + string.digits, k=(random.randint(10, 30))))
        _trash_list.append(_piece_of_trash)
    prose_array = []
    for i in range(12):
        prose_array.append("_{}_AAA\nBBB\nCCC".format(''.join(random.choices(string.ascii_uppercase + string.digits, k=(random.randint(4, 10))))))

    pp([["newline sanity test\nSource text\n"],
        {"indent":0, "columns":1}, [prose_array[0]],{"indent":0}, ["\nNewlines are respected only if its a single item on no indent!\n\nResult:"],
        {"columns":2, "indent":1}, prose_array])

    divider_function("Ending test 'printing_newlines'")

    pp([["Printing items in a 2 column adaptive layout"], {"indent": 1, "columns": 2, "column_width": 3, "filler": "."},_trash_list])
    pp([["Printing trash in a 3 column restrictive layout"],{"indent": 1, "columns": 3, "column_width": 5, "force_width": True, "filler": "-"}, _trash_list])
    pp([["Printing items in a narrow 5 column restrictive name-sorted layout"],{"key": lambda x : x ,"indent": 1, "columns": 5, "column_width": 3, "force_width": True, "filler": "."}, _trash_list])

    pp([["Length-sorting"], {"indent": 1, "columns": 1, "key": lambda x: len(x)}, _trash_list])
    pp([["Reverse-length-sorting"], {"indent": 1, "columns": 1, "key": lambda x: len(x), "reverse": True}, _trash_list])
    pp([["Unsorted single-column"], {"indent": 1, "columns": 1}, _trash_list])

    divider_function("Ending test 'printing and sorting'")

def inspector(r):
    divider_function("Beginning test 'inspector'")

    e = ECS.Entity(r)
    e.grant(ECS.Component(r, "color"))
    e.grant(ECS.Component(r, "position", 10, 15))
    e.grant(ECS.Component(r, "age"))
    #tools.inspect(e)
    tools.inspect(e.components["position"])
    divider_function("Ending test 'inspector'")

def ecs_systems(r):
    divider_function("Beginning test 'ecs_systems'")

    e = ECS.Entity(r)
    e.grant(ECS.Component(r, "color"))
    e.grant(ECS.Component(r, "position", 10, 15))
    e.grant(ECS.Component(r, "age"))

    divider_function("Ending test 'ecs_systems'")