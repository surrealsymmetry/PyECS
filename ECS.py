import ECS_blueprints as blueprints
import pwint
pp = pwint.pwint

###
### an Entity is a container for a cluster of components arranged by aspect key
###
class Entity:
    def __init__(self, r, *args, **kwargs):
        self.components = {}
        r.register(self, *args, **kwargs)
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
        r.register(self, *args, **kwargs)

    def __repr__(self):
        return "OBJ {}".format(self.id)


class System:
    def __init__(self, r, key_profile, function_profile, name="UNNAMED", *args, **kwargs):  # ordered tuples
        self.function_profile = function_profile
        self.key_profile = key_profile
        self.name = name
        r.register(self, *args, **kwargs)

    def update(self):
        # print("{} ({}) Update".format(self.id, self.name))
        for f in self.function_profile:
            if callable(f):
                f()
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

        """msg = 0
        for key in self.components:
            msg += len(self.components[key])
        msg = "\n\tC|\t" + str(msg) + "\t({} keys)".format(len(self.components))
        msg = "\n\tE|\t" + str(len(self.entities)) + msg + "\n\tS|\t" + str(len(self.systems))"""
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
        if "doc" in kwargs:
            doc = kwargs["doc"]
            doc.append({"indent": 1})
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
