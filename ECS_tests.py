import ECS
import random
import string


def mob_spawn(r):
    my_entities = []
    component_keys = []
    for i in range(1000):
        my_entities.append(r.register(ECS.Entity()))

    for i in range(10):
        component_keys.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))

    for i in my_entities:
        i.grant(r.register(ECS.Component("dummy")))
        components_to_install = random.randint(3, 5)
        done_selecting = False
        while not done_selecting:
            c_to_add = component_keys[random.randint(0, len(component_keys) - 1)]
            if c_to_add not in i.components:
                i.grant(r.register(ECS.Component(c_to_add)))
                components_to_install -= 1
                if components_to_install <= 0:
                    done_selecting = True
        print("{} granted {} components".format(i.id, len(i.components)))
    print(r)

