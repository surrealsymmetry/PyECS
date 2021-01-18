import ECS_blueprints as blueprints
import pwint
pp = pwint.pwint

###
### an Entity is a container for a cluster of components arranged by aspect key
###
class Entity:
    def __init__(self):
        self.components = {}
    def __repr__(self):
        return "OBJ {}".format(self.id)

    def grant(self, c):
        if c.key in self.components:
            print("key {} already exists in entity {}! values being overwritten! ")
        self.components[c.key] = c
        c.entity = self
        return c

###
### a Component is an instance of data state defined by aspect key (eg "position" has an x and y value)
### components compose the state properties of objects
###
class Component:
    def __init__(self, key, *args):
        assert type(key) is str and len(key) > 0, "Component provided invalid aspect key '{}'".format(key)
        self.key = key
        if key in blueprints.components:
            # keyed to a method lookup that will stamp preset attributes onto this instance of c
            blueprints.components.get(key)(self, *args)

    def __repr__(self):
        return "OBJ {}".format(self.id)

class System:
    def __init__(self, *args):
        self.keys = []
        self.functions = []
        for arg in args:
            self.load(arg)

    def load(self, arg):
        if type(arg) is str:
            self.keys.append(arg)
        elif callable(arg):
            self.functions.append(arg)
        else:
            try:
                iterable_argument = iter(arg)
                for i in arg:
                    self.load(i)
            except TypeError:
                raise TypeError("unknown type passed to system.load()")

    def update(self, r):
        subscribed_entities = []
        first_element_rack = r.components[self.keys[0]]

        for id_key in first_element_rack:
            c = first_element_rack[id_key]
            meets_requirements = True
            for i in range(1, len(self.functions) - 1):
                if self.keys[i] not in c.entity.components:
                    meets_requirements = False
            if meets_requirements:
                subscribed_entities.append(c.entity)

        for e in subscribed_entities:
            assert type(e) == Entity, ("Non-Entity object {} pulled into {} subscription queue?".format(e, self.name))
            for f in self.functions:
                if callable(f):
                    f(e)
                else:
                    print("uncallable object in system function profile")


class Rack:
    def __init__(self):
        self.entities = {}
        self.components = {}
        self.systems = {}
        self.registry_keyring = {}

    ### IDs are stamped on objects passed to rack.register()
    ### ID counter categories will by dynamically issued by class
    def __fresh_id(self, class_key):  # only gets called by r.register
        if class_key not in self.registry_keyring:
            self.registry_keyring[class_key] = 0
        fresh_id = "{}_{}".format( class_key[0:1], self.registry_keyring[class_key])
        self.registry_keyring[class_key] += 1
        return fresh_id

    def e(self):
        e = Entity()
        self.register(e)
        return e
    def c(self, key, *args):
        c = Component(key, *args)
        self.register(c)
        return c
    def s(self, name, *args):
        s = System(args)
        s.name = name
        self.register(s)
        return s

    def register(self, o):  # punches an ID onto every tracked object
        o.id = self.__fresh_id(type(o).__name__)
        o.purge = lambda x: self.purge(x)

        def switch_e():
            self.entities[o.id] = o
        def switch_c():
            o.id = "{}_{}".format(o.id, o.key)
            if o.key not in self.components:
                self.components[o.key] = {}
            self.components[o.key].update({o.id: o})
        def switch_s():
            o.id = "{}_{}".format(o.id, o.name)
            self.systems[o.id] = o

        {"Entity": switch_e, "Component": switch_c, "System": switch_s}[type(o).__name__]()


    def purge(self, o):
        print("\nPurging ", o.id)

        def switch_e():
            component_cluster = {}
            for key in o.components:
                component_cluster.update({key: o.components[key].id})
            for key in component_cluster:
                self.components[key].pop(component_cluster[key])

            self.entities.pop(o.id)
            print("\tDeleted {}\n\tDeleted {}".format(o, list(component_cluster)))
            return component_cluster

        def switch_c():
            print("Purging Component {}".format(o.id))
            switch_e(self.entity)

        def switch_s():
            print("switch s")
            self.systems.pop(o.id)

        {"Entity": switch_e, "Component": switch_c, "System": switch_s}[type(o).__name__]()

    def update(self):
        for id_key in self.systems:
            self.systems[id_key].update(self)