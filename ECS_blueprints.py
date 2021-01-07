import random
import pwint
pp = pwint.pwint
import datetime

components = {}
def position(c, x=0, y=0):
    c.x = x
    c.y = y
    pp([["position"],{"columns":2,"indent":1},["x",c.x,"y",c.y]], preserve=True)
    return c


def color(c):
    def randcolor():
        return(random.randint(0,255))
    c.color = (randcolor(), randcolor(), randcolor())
    c.colors = {"bg": (81, 75, 83),
               "hot": (238,160, 185)}

def age(c):
    c.created = datetime.datetime.now()

components.update({"position": lambda x, *args: position(x, *args),
                   "color": lambda x, *args: color(x, *args),
                   "age": lambda x, *args: age(x, *args)})
