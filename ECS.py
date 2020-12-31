import ECS_blueprints as blueprints


###
### an Entity is a container for a cluster of components arranged by aspect key
###
class Entity:
    def __init__(self):
        print("\nNew entity")
        self.components = {}

    def __repr__(self):
        return "OBJ {}".format(self.id)

    def grant(self, c):
        if c.key in self.components:
            print("key {} already exists in entity {}! values being overwritten! ")
        self.components[c.key] = c
        c.entity = self
        print("\t\tstamped imprint '{}'".format(c.entity.id))
        return c


###
### a Component is an instance of data state defined by aspect key (eg "position" has an x and y value)
### components compose the state properties of objects
###
class Component:
    def __init__(self, key):
        print("\nNew component '{}'".format(key))
        assert type(key) is str
        self.key = key

        if key in blueprints.components:
            print("\tknown definition '{}' accepted\n\tinvoking {}({})".format(key, blueprints.components[key],
                                                                               type(self).__name__))
            blueprints.components.get(key)(self)

    def __repr__(self):
        return "OBJ {}".format(self.id)


class System:
    def __init__(self, key_profile, function_profile, name="UNNAMED"):  # ordered tuples
        print("New system")
        self.function_profile = function_profile
        self.key_profile = key_profile
        self.name = name

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
        msg = 0
        for key in self.components:
            msg += len(self.components[key])
        msg = "\n\tC|\t" + str(msg) + "\t({} keys)".format(len(self.components))
        msg = "\n\tE|\t" + str(len(self.entities)) + msg + "\n\tS|\t" + str(len(self.systems))
        return msg

    ### IDs are stamped on objects passed to rack.register()
    ### ID counter categories will by dynamically issued by class

    def __fresh_id(self, key):  # only gets called by r.register
        if key not in self.registry_keyring:
            self.registry_keyring[key] = 0
        fresh_id = "{}_{}".format(key, self.registry_keyring[key])
        self.registry_keyring[key] += 1
        return fresh_id

    def purge(self, o):
        print("\nPurging ", o.id)

        def _switch_e():
            component_cluster = {}
            for key in o.components:
                component_cluster.update({key: o.components[key].id})
            for key in component_cluster:
                self.components[key].pop(component_cluster[key])

            self.entities.pop(o.id)
            print("\tDeleted {}\n\tDeleted {}".format(o, list(component_cluster)))
            return component_cluster

        def _switch_c():
            print("switch c")
            _switch_e(self.entities[o.entity])

        def _switch_s():
            print("switch s")
            self.systems.pop(o.id)

        return {"Entity": _switch_e, "Component": _switch_c, "System": _switch_s}[type(o).__name__]()

    def register(self, o):  # punches an ID onto every tracked object
        print("\tregistering {}".format(type(o).__name__))
        o.id = self.__fresh_id(type(o).__name__)

        if type(o) is Entity:
            self.entities[o.id] = o
        elif type(o) is Component:
            o.id = "{}_{}".format(o.id, o.key)
            if o.key not in self.components:
                self.components[o.key] = {}
            self.components[o.key].update({o.id: o})
        elif type(o) is System:
            o.id = "{}_{}".format(o.id, o.name)
            self.systems[o.id] = o
        else:
            print("unknown object passed to rack.register")
        o.purge = lambda x: self.purge(x)
        print("\t\tstamped '{}'\n\t\tstamped purge()".format(o.id))
        return o
