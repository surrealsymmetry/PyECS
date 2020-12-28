import ECS
import random
import string


def mob_spawn(r, e_spawn=1000, k_spawn=100):
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

    def murderbot(c_to_nuke=30):
        print("murderbot online")
        component_keys_to_nuke = []
        done_selecting = False
        while not done_selecting:
            random_component_key = list(r.components.keys())[random.randint(0, len(r.components) - 1)]
            if random_component_key not in component_keys_to_nuke and random_component_key != "dummy":
                component_keys_to_nuke.append(random_component_key)
                if len(component_keys_to_nuke) >= c_to_nuke or len(component_keys_to_nuke) == len(r.components) - 1:
                    done_selecting = True
            else:
                print("\tseeking new target...")
        print("\n{} targets Acquired!".format(len(component_keys_to_nuke)))
        nuke = {}
        for i in component_keys_to_nuke:
            #print("\t{}:\t{} instances".format(i, len(r.components[i])))
            #print(r.components[i])
            for key in r.components[i]:
                target_c_id = r.components[i].get(key).id
                #print("popping ", target_c_id, "of entity", r.components[i].get(target_c_id).entity )
                e = r.components[i].get(target_c_id).entity
                e_id = r.components[i].get(target_c_id).entity.id
                nuke.update({e_id : e})







    f = murderbot
    s = r.register(ECS.System(("dummy",), (f,)))
    s.update()

    print(r)
