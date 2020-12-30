import ECS
import ECS_tools as tools
import random
import string


def divider_function(msg):
    print("{:-^70}".format(msg))

def populate_manipulate(r, e_spawn=15, k_spawn=9):
    divider_function("Beginning test 'populate_manipulate'")

    my_entities = []
    component_keys = []
    for i in range(e_spawn):
        my_entities.append(r.register(ECS.Entity()))

    for i in range(k_spawn):
        component_keys.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=(random.randint(5,10)))))

    for i in my_entities:
        i.grant(r.register(ECS.Component("dummy")))
        components_to_install = random.randint(3, 3)
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
        tools.inspect_entity(r.entities[racked_entities[rand_num_in_range]])

    inspect_random_entity()
    inspect_random_entity()
    inspect_random_entity()



    #while len(r.entities) > 0:
        #s.update()
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
    tools.inspect_entity(e)
    print("\t Entity is at X: {} Y:{}".format(e.components["position"].x, e.components["position"].y))

    e_2 = spawn_one()
    e_2.grant(r.register(ECS.Component("color")))
    tools.inspect_entity(e_2)
    print("\nColour 'Hot'\n\tRED:\t{}\n\tGREEN:\t{}\n\tBLUE:\t{}".format(
        e_2.components["color"].colors["hot"][0],
        e_2.components["color"].colors["hot"][1],
        e_2.components["color"].colors["hot"][2]))
    divider_function("Ending test 'blueprinting'")
    return r

def inspecting(r):
    divider_function("Starting test 'inspecting'")
    e = r.register(ECS.Entity())
    e.grant(r.register(ECS.Component("color")))

    tools.inspect_rack(r)

    for id_key in r.components["dummy"]:
        tools.inspect_entity(r.components["dummy"].get(id_key).entity)

    # tools.inspect_rack(r)
    # tools.inspect_entity(e)
    divider_function("Ending test 'inspecting'")
    return r
