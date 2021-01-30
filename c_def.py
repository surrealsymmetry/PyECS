import random
import datetime
import pygame

def __kwarg_constructor(c, **kwargs):
    for k in kwargs:
        assert hasattr(c, k), \
            "Component blueprint {} passed invalid keyword {} during {} construction".format(c.key, k, c.id)
        setattr(c, k, kwargs[k])
    return c

def box(c, *args):
    if len(args) > 0:
        assert len(args) == 2, "bounds component intitialized with ILLEGAL number of arguments"
        c.x = args[0]
        c.y = args[1]
    else:
        c.x = 0
        c.y = 0
    return c

def vector2(c, x=0, y=0):
    c.x = x
    c.y = y
    return c

def position(c, *args):
    vector2(c, *args)
    return c

def momentum(c, *args):
    vector2(c, *args)
    return c

def color(c):
    def randcolor():
        return random.randint(0, 255)
    c.color = (randcolor(), randcolor(), randcolor())
    return c

def age(c):
    c.created = datetime.datetime.now()


def sprite(c):

    return c

def particle_source(c, **kwargs):
    c.max = 0
    c.rate = 1
    __kwarg_constructor(c, **kwargs)
    c.particles = []
    return c

def particle(c, source = None):
    if source:
        assert type(source) is str
    c.source = source
    return c

def timer_countdown(c, lifespan=0):
    c.remaining = lifespan
    return c

def pygame_global_timer(c):
    c.delta = 0
    c.total = 0
    return c
