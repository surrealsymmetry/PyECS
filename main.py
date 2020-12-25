class Entity:
    def __init__(self, id):
        print("\tE\tinstance initiated with id",id)
        assert type(id) is int
        self.id = id
        self.components = {}

    def grant(self, c):
        self.components[c.key] = c
        print("\tE\t%s\tgranted C\t'%s'\t%s" % (self.id, c.key, c.id))
        c.entity = self
        return c


class Component:
    def __init__(self, key, id):
        print("\tC\tinstance initiated with id %s and key '%s'" % (id, key))
        assert type(key) is str
        assert type(id) is int
        self.key = key
        self.id = id


class Rack:

    def __init__(self):
        print("\tR\tinstance initiated")
        self.entities = {}
        self.components = {}
        self.e_id = 0
        self.c_id = 0

    def __repr__(self):
        element_totals = "\tE:\t"+str(self.e_id)+"\n\tC:\t"+str(self.c_id)
        return element_totals

    def request_entity(self):
        e = Entity(self.e_id)
        self.e_id += 1
        self.entities.update({self.e_id: e})
        return e

    def request_component(self, key):
        c = Component(key, self.c_id)
        self.c_id += 1
        if c.key in self.components.keys() :
            self.components[c.key] = c
            print("\tC:\t",c.key,"racked")
        else:
            self.components.update({c.key:[c]})
            print("\tC:\track entry '%s' added" % (c.key))
        return c


print("Creating instance of class Rack")
my_rack = Rack()
my_entity = my_rack.request_entity()
my_entity.grant(my_rack.request_component("dummy"))
print(my_rack)
