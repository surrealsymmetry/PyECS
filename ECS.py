import ECS_blueprints as blueprints

class Entity:
    def __init__(self):
        self.components = {}

    def __repr__(self):
        return "OBJ "+self.id

    def grant(self, c):
        if c.key in self.components:
            print("key {} already exists in entity {}! values being overwritten! ")
        self.components[c.key] = c
        c.entity = self
        return c


class Component:
    def __init__(self, key):
        assert type(key) is str
        self.key = key

        ### if key in blueprint library
        ### retrieve the lambda as a value
        ### operate on c with it

        if key in blueprints.components:
            print("Blueprint definition '{}' accepted\n\tcalling {} with argument {}".format(key, blueprints.components[key], type(self).__name__))
            blueprints.components.get(key)(self)


    def __repr__(self):
        return "{}_{}_OBJ".format(self.id, self.key)


class System:
    def __init__(self, key_profile, function_profile, name="UNNAMED"):  # ordered tuples
        self.function_profile = function_profile
        self.key_profile = key_profile
        self.name = name

    def update(self):
        #print("{} ({}) Update".format(self.id, self.name))
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


    def fresh_id(self, key):  # keys for this
        if key not in self.registry_keyring:
            self.registry_keyring[key] = 0
        fresh_id = "{}_{}".format(key, self.registry_keyring[key])
        self.registry_keyring[key] += 1
        return fresh_id

    def purge(self, o):
        print("\tPurging ", o.id)

        def _switch_e():
            graveyard = {}
            for key in o.components:
                graveyard.update({key: o.components[key].id})
            for key in graveyard:
                self.components[key].pop(graveyard[key])
            self.entities.pop(o.id)
            print("\tDeleted {} and {} components".format(o, len(graveyard)))
            return graveyard

        def _switch_c():
            print("switch c")
            _switch_e(self.entities[o.entity])

        def _switch_s():
            print("switch s")
            self.systems.pop(o.id)

        return {"Entity": _switch_e, "Component": _switch_c, "System": _switch_s}[type(o).__name__]()

    def register(self, o):
        o.id = self.fresh_id(type(o).__name__)

        if type(o) is Entity:
            self.entities[o.id] = o
        elif type(o) is System:
            self.systems[o.id] = o
        elif type(o) is Component:
            if o.key not in self.components:
                self.components[o.key] = {}
                # print("\tnew rack c '%s'" % (o.key))
            self.components[o.key].update({o.id: o})
            # print("\tracked component", o.id)
        else:
            print("unknown object passed to rack.register")
        o.abort = lambda x : self.purge(o)
        return o

