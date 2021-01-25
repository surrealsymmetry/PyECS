import random
import datetime
import pygame

def bounds(c, *args):
    if len(args) > 0:
        assert len(args) == 2, "bounds component intitialized with ILLEGAL number of arguments"
        c.x = args[0]
        c.y = args[1]
    else:
        c.x = 0
        c.y = 0
    return c

def position(c, *args):
    if len(args) > 0:
        assert len(args) == 2, "position component intitialized with ILLEGAL number of arguments"
        c.x = args[0]
        c.y = args[1]
    else:
        c.x = 0
        c.y = 0
    return c


def color(c):
    def randcolor():
        return random.randint(0, 255)

    c.color = (randcolor(), randcolor(), randcolor())
    c.colors = {"bg": (81, 75, 83),
                "hot": (238, 160, 185)}


def age(c):
    c.created = datetime.datetime.now()


def graphic(c, **kwargs):
    attr = {
        'bounds': None,
        'sprite': None,
        'layer': 0}

    for key in kwargs:
        attr.update({key: kwargs[key]})

    for key in attr:
        setattr(c, key, attr[key])

    return c


def timer(c):
    c.delta = 0
    c.total = 0

