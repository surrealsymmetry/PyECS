import ECS
import string
import random

r = ECS.Rack()
my_entities = []
component_keys = []
for i in range(100):
    my_entities.append(r.request_entity())

for i in range(25):
    component_keys.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))

for i in my_entities:
    i.grant(r.request_component("dummy"))
    components_to_install = random.randint(3, 10)
    done_selecting = False
    while not done_selecting:
        c_to_add = component_keys[random.randint(0, len(component_keys) - 1)]
        if c_to_add not in i.components:
            i.grant(r.request_component(c_to_add))
            #print("\tadded!")
            components_to_install -= 1
            if components_to_install <= 0:
                done_selecting = True
    print("{} granted {} components".format(i.id, len(i.components)))
print(r)
