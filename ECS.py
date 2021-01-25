import c_def
import rack
###
### an Entity is a container for a cluster of components arranged by aspect key
###
class Entity:
    def __init__(self, *args):
        self.components = {}

        for arg in args:
            if len(args) > 0:
                if isinstance(arg, Component):
                    self.grant(arg)
                elif type(arg) is str:
                    i = Component(arg)
                    self.grant(i)
                else:
                    try:
                        iterable_thing = iter(arg)
                        for i in arg:
                            if type(i) is str:
                                i = Component(i)
                            else:
                                assert isinstance(arg, Component), "Entity constructor passed an iterable arg with a non-Component inside"
                            self.grant(i)
                    except TypeError:
                        raise TypeError("Entity constructor passed non iterable, non-Component arg")

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
    def __init__(self, key, *args, **kwargs):
        assert type(key) is str and len(key) > 0, "Component provided invalid aspect key '{}'".format(key)
        self.key = key
        if hasattr(c_def, key):
            print("Component: Definition '{}' initialized".format(key))
            getattr(c_def, key)(self, *args, **kwargs)
        else:
            print("Component: Undefined '{}' initialized".format(key))

    def __repr__(self):
        return "OBJ {}".format(self.id)

class System:
    def __init__(self, *args):
        self.keys = []
        self.functions = []
        for arg in args:
            self.__load(arg)

    #seperate args into keys or functions
    def __load(self, arg):
        if type(arg) is str:
            self.keys.append(arg)
        elif callable(arg):
            self.functions.append(arg)
        else:
            try:
                iterable_argument = iter(arg)
                for i in arg:
                    self.__load(i)
            except TypeError:
                raise TypeError("unknown type passed to system.load()")

    def update(self, subscribed_set):
        for e in subscribed_set:
            assert type(e) == Entity, ("Non-Entity object {} pulled into {} subscription queue?".format(e, self.name))
            for f in self.functions:
                if callable(f):
                    f(e)
                else:
                    print("uncallable object {} in system function profile".format(f))


