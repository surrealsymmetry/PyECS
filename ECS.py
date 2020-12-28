class Entity:
    def __init__(self):
        self.components = {}
    def __repr__(self):
        return self.id

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
    def __repr__(self):
        return "{}_{}".format(self.id,self.key)


class System:
    def __init__(self, key_profile, function_profile):  # ordered tuples
        self.function_profile = function_profile
        self.key_profile = key_profile

    def update(self):
        print(self.id+" update")
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

    def __repr__(self):  # overrides the output of print(rack_object)
        msg = 0
        for key in self.components:
            msg += len(self.components[key])
        msg = "\n\tC|\t" + str(msg) + "\t({} keys)".format(len(self.components))
        msg = "\n\tE|\t" + str(len(self.entities)) + msg + "\n\tS|\t" + str(len(self.systems))
        return msg

    registry_keyring = {}

    @staticmethod
    def fresh_id(key):  # keys for this
        if key not in Rack.registry_keyring:
            Rack.registry_keyring[key] = 0
        fresh_id = "{}_{}".format(key, Rack.registry_keyring[key])
        Rack.registry_keyring[key] += 1
        return fresh_id

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
        return o

    #def purge(self):