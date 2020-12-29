import ECS
import ECS_tools as tools
import random
import string


def populate_manipulate(e_spawn=1000, k_spawn=100):
    r = ECS.Rack()
    my_entities = []
    component_keys = []
    for i in range(e_spawn):
        my_entities.append(r.register(ECS.Entity()))

    for i in range(k_spawn):
        component_keys.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))

    for i in my_entities:
        i.grant(r.register(ECS.Component("dummy")))
        components_to_install = random.randint(1, 10)
        done_selecting = False
        while not done_selecting:
            c_to_add = component_keys[random.randint(0, len(component_keys) - 1)]
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

    def divider_function():
        print("\tmurder ~uwu~\n")

    function_profile = (murderbot, divider_function)
    s = r.register(ECS.System(("dummy",), (function_profile), "murderbot"))

    while len(r.entities) > 0:
        s.update()
    print(r)
    del r

def pygame_implementation():
    import pygame
    import ECS_blueprints
    r = ECS.Rack()

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
    print("Colour 'Hot'\n\tRED:\t{}\n\tGREEN:\t{}\n\tBLUE:\t{}".format(
        e_2.components["color"].colors["hot"][0],
        e_2.components["color"].colors["hot"][1],
        e_2.components["color"].colors["hot"][2]))


