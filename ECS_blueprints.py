components = {}

def say(o):
    print("\t\tconstructing '{}' data".format(o.key))

def position(c):
    say(c)
    c.x = 0
    c.y = 0
    return c


def color(c):
    say(c)
    c.colors = {"bg": (81, 75, 83),
               "hot": (238,160, 185)}

components.update({"position": lambda x: position(x),
                   "color": lambda x: color(x)})
