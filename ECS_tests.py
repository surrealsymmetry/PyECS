import ECS
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
        print(r.purge(r.entities[list(r.entities.keys())[random.randint(0,len(r.entities))]]))

    def divider_function():
        print("\tmurder ~uwu~\n")
    function_profile = (murderbot, divider_function)
    s = r.register(ECS.System(("dummy",), (function_profile), "murderbot"))
    s.update()
    s.update()

    print(r)

def pygame_implementation():
    import pygame

