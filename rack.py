import ECS
import ECS_Inspector as tools
entities = {}
components = {}
systems = {}
registry_keyring = {}



def e(*args, **kwargs):
    e = ECS.Entity(*args, **kwargs)
    register(e)
    return e

def c(key, *args, **kwargs):
    c = ECS.Component(key, *args, **kwargs)
    register(c)
    return c
def s(name, *args):
    s = ECS.System(*args)
    s.name = name
    register(s)
    return s

### IDs are stamped on objects passed to rack.register()
### ID counter categories will by dynamically issued by class
def __fresh_id(class_key):  # only gets called by r.register
    if class_key not in registry_keyring:
        registry_keyring[class_key] = 0
    fresh_id = "{}_{}".format( class_key[0:1], registry_keyring[class_key])
    registry_keyring[class_key] += 1
    return fresh_id

def register(o):  # punches an ID onto every tracked object
    o.id = __fresh_id(type(o).__name__)
    o.purge = lambda x: purge(x)

    def switch_e():
        entities[o.id] = o
        print("racked entity", o.id)
    def switch_c():
        o.id = "{}_{}".format(o.id, o.key)
        if o.key not in components:
            components[o.key] = {}
        components[o.key].update({o.id: o})
        print("racked component", o.id)
    def switch_s():
        o.id = "{}_{}".format(o.id, o.name)
        systems[o.id] = o
        print("racked system", o.id)

    {"Entity": switch_e, "Component": switch_c, "System": switch_s}[type(o).__name__]()

def purge(o):
    print("\nPurging ", o.id)

    def switch_e():
        component_cluster = {}
        for key in o.components:
            component_cluster.update({key: o.components[key].id})
        for key in component_cluster:
            components[key].pop(component_cluster[key])

        entities.pop(o.id)
        print("\tDeleted {}\n\tDeleted {}".format(o, list(component_cluster)))
        return component_cluster

    def switch_c():
        print("Purging Component {}".format(o.id))
        purge(o.entity)

    def switch_s():
        print("switch s")
        systems.pop(o.id)

    {"Entity": switch_e, "Component": switch_c, "System": switch_s}[type(o).__name__]()

def update():
    for id_key in systems:
        sys = systems[id_key]
        subscribed_set = []

        if  sys.keys[0] in components:
            first_element_rack = components[sys.keys[0]]

            for id_key in first_element_rack:
                c = first_element_rack[id_key]
                meets_requirements = True
                if hasattr(c, 'entity'):
                    for i in range(len(sys.keys)):
                        if sys.keys[i] not in c.entity.components:
                            meets_requirements = False
                else:
                    meets_requirements = False
                    print("loose component {}".format(c.id))

                if meets_requirements:
                    subscribed_set.append(c.entity)

        sys.update(subscribed_set)