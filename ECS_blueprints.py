components = {}


def position(c):
    print("\tBlueprinting POSITION on new component")
    c.x = 0
    c.y = 0
    return c


def color(c):
    print("\tBlueprinting COLOR on new component")
    c.colors = {"bg": (81, 75, 83),
               "hot": (238,160, 185)}

components.update({"position": lambda x: position(x),
                   "color": lambda x: color(x)})
