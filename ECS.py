import ECS_blueprints as blueprints
import pwint
pp = pwint.pwint

###
### an Entity is a container for a cluster of components arranged by aspect key
###
class Entity:
    def __init__(self, r, *args, **kwargs):
        self.components = {}
        r.register(self)
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
    def __init__(self, r, key, *args, **kwargs):
        assert type(key) is str and len(key) > 0, "Component provided invalid aspect key '{}'".format(key)
        self.key = key
        if key in blueprints.components:
            # keyed to a method lookup that will stamp preset attributes onto this instance of c
            blueprints.components.get(key)(self, *args)
        r.register(self)

    def __repr__(self):
        return "OBJ {}".format(self.id)


class System:
    def __init__(self, r, name, *args, **kwargs):  # ordered tuples
        assert type(r) == Rack, "systems must be passed a rack object as first parameter, not {}".format(type(r))
        self.name = name
        self.aspect_requirements = []
        for arg in args:
            assert type(arg) == str, "non string passed to system constructor aspect requirement arg list"
            self.aspect_requirements.append(arg)

        if "function_profile" in kwargs:
            self.function_profile = kwargs["function_profile"]
        else:
            self.function_profile = []
        r.register(self, *args, **kwargs)

    def update(self, r):
        subscribed_entities = []
        first_element_rack = r.components[self.aspect_requirements[0]]

        for id_key in first_element_rack:
            c = first_element_rack[id_key]
            meets_requirements = True
            for i in range(1, len(self.aspect_requirements) - 1):
                if self.aspect_requirements[i] not in c.entity.components:
                    meets_requirements = False
            if meets_requirements:
                subscribed_entities.append(c.entity)

        for e in subscribed_entities:
            assert type(e) == Entity, ("Non-Entity object {} pulled into {} subscription queue?".format(e, self.name))
            for f in self.function_profile:
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

    def __repr__(self):  # overrides the output of print(rack_object)
        msg = "r"
        doc = []

        return msg

    ### IDs are stamped on objects passed to rack.register()
    ### ID counter categories will by dynamically issued by class

    def __fresh_id(self, class_key):  # only gets called by r.register
        if class_key not in self.registry_keyring:
            self.registry_keyring[class_key] = 0
        fresh_id = "{}_{}".format( class_key[0:1], self.registry_keyring[class_key])
        self.registry_keyring[class_key] += 1
        return fresh_id

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
            switch_e(self.entities[o.entity])

        def switch_s():
            print("switch s")
            self.systems.pop(o.id)

        {"Entity": switch_e, "Component": switch_c, "System": switch_s}[type(o).__name__]()

    def register(self, o, *args, **kwargs):  # punches an ID onto every tracked object
        o.id = self.__fresh_id(type(o).__name__)
        o.purge = lambda x: self.purge(x)
        doc = []

        doc.append({"columns":4, "column_width":20, "filler":"."})
        def switch_e():
            self.entities[o.id] = o
            doc.append(["registering {}".format(o.id)])
        def switch_c():
            o.id = "{}_{}".format(o.id, o.key)
            new_rack = ""
            if o.key not in self.components:
                self.components[o.key] = {}
            self.components[o.key].update({o.id: o})
            doc.append(["registering {}".format(o.id)])
            doc.append({"indent":1})
        def switch_s():
            o.id = "{}_{}".format(o.id, o.name)
            self.systems[o.id] = o
            doc.append(["registering {}".format(o.id)])

        {"Entity": switch_e, "Component": switch_c, "System": switch_s}[type(o).__name__]()
        pp(doc)

    def update(self):
        for id_key in self.systems:
            self.systems[id_key].update(self)