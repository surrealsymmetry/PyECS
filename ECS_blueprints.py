import random
import datetime

components = {}

def position(c, *args):

    if len(args) > 0:
        assert len(args) == 2, "position component intitialized with ILLEGAL number of arguments"

    c.x = args[0]
    c.y = args[1]
    return c


def color(c):
    def randcolor():
        return(random.randint(0,255))
    c.color = (randcolor(), randcolor(), randcolor())
    c.colors = {"bg": (81, 75, 83),
               "hot": (238,160, 185)}

def age(c):
    c.created = datetime.datetime.now()

components.update({"position"   : lambda x, *args: position(x, *args),
                   "color"      : lambda x, *args: color(x, *args),
                   "age"        : lambda x, *args: age(x, *args)
                   })
