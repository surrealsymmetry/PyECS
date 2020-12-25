class Entity:
    def __init__(self):
        self.components = {}

    def grant(self, c):
        self.components[c.key] = c
        c.entity = self
        c.entity = self
        return c


class Component:
    def __init__(self, key):
        assert type(key) is str
        self.key = key


class Rack:
    def __init__(self):
        self.entities = []
        self.components = {}

    def __repr__(self):  # overrides the output of print(rack_object)
        component_counter = 0
        key_list = ""
        tally_dict = {}
        for key in self.components:
            component_counter += len(self.components[key])
            if key not in tally_dict.keys():
                tally_dict[key] = 0
            tally_dict[key] += len(self.components[key])
            key_list = key_list + ("\n\t\t\t\t" + str(tally_dict[key]) + "  '" + str(key) + "'")
        msg = "\tE:\t" + str(len(self.entities)) + "\n\tC:\t" + str(len(self.components)) + " keys\t" + str(
            component_counter) + " components" + key_list
        return msg

    def request_entity(self):
        e = Entity()
        self.entities.append(e)
        return e

    def request_component(self, key):
        c = Component(key)
        if c.key in self.components.keys():
            self.components[c.key].append(c)  # appending to the table that is the value of the key
        else:
            self.components.update({c.key: [c]})
            #print("\track entry '%s' added" % (c.key))
        return c