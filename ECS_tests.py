import ECS
import ECS_Inspector as tools
import random
import string
import datetime
import pwint
import pygame

pp = pwint.pwint


def divider_function(msg):
    _deco = "~~"
    print("{}{:-^70}{}".format(_deco, msg, _deco))


def blueprinting(r):
    divider_function("Beginning test 'blueprinting'")

    def spawn_one():
        e = ECS.Entity(r)
        c = ECS.Component(r, "position")
        c.x = 3
        e.grant(c)

        return e

    e = spawn_one()

    tools.inspect(e)
    print("\t Entity is at X: {} Y:{}".format(e.components["position"].x, e.components["position"].y))

    e_2 = spawn_one()
    e_2.grant(ECS.Component(r, "color"))

    tools.inspect(e_2)
    tools.inspect(e_2.components["color"])

    print("\nColour 'Hot'\n\tRED:\t{}\n\tGREEN:\t{}\n\tBLUE:\t{}".format(
        e_2.components["color"].colors["hot"][0],
        e_2.components["color"].colors["hot"][1],
        e_2.components["color"].colors["hot"][2]))
    divider_function("Ending test 'blueprinting'")
    return r


def printing_and_sorting(r):
    divider_function("Starting test 'printing and sorting'")
    f_nam = ["becky", "noah", "bri", "jasper", "colin", "sandra", "peppin", "eleanor", "chester", "angelina", "grint",
             "oswald", "fiona", "parker", "trisha", "joanne", "serena"]
    l_nam = ["dreck", "berd", "auren", "suarez", "peach", "duard", "nona", "poleck", "merino", "grant", "chi", "decker",
             "wolf", "khan", "smith", "durent", "blunt", "parcey"]
    for i in range(len(f_nam)):
        for j in range(len(l_nam)):
            c = ECS.Component(r, "name")  # doc=[["Component Spawning:"]])
            c.name = "{} {}".format(f_nam[i], l_nam[j])
            e = ECS.Entity(r)  # doc=[["Entity Spawning:"]])
            e.grant(c)
            # print("{}\t{} {}".format(e.id, e.components["name"].name[0], e.components["name"].name[1]))

    print("{} entities spawned".format(len(r.entities)))

    list = []
    for key in r.entities:
        e = r.entities[key]
        if "name" in e.components:
            name = e.components["name"].name
            list.append("{} : {}".format(e.id, name))

    pp([["Unsorted"], {"columns": 4, "column_width": 20, "indent": 1}, list])
    pp([["Last Name Sort"], {"columns": 4, "column_width": 20, "indent": 1,
                             "key": lambda x: x.split(" ")[3]}, list])
    pp([["Reverse First Name Sort"], {"columns": 4, "column_width": 20, "indent": 1,
                                      "key": lambda x: x.split(" ")[2], "reverse": True}, list])
    pp([["Name Length Sort"], {"columns": 4, "column_width": 20, "indent": 1,
                               "key": lambda x: len(x.split(" ")[2] + x.split(" ")[3])}, list])

    _trash_list = []
    for i in range(20):
        _piece_of_trash = ''.join(random.choices(string.ascii_uppercase + string.digits, k=(random.randint(3, 10))))
        _trash_list.append(_piece_of_trash)
        _piece_of_trash = ''.join(random.choices(string.ascii_uppercase + string.digits, k=(random.randint(10, 30))))
        _trash_list.append(_piece_of_trash)
    prose_array = []
    for i in range(12):
        prose_array.append("_{}_AAA\nBBB\nCCC".format(
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=(random.randint(4, 10))))))

    pp([["newline sanity test\nSource text\n"],
        {"indent": 0, "columns": 1}, [prose_array[0]], {"indent": 0},
        ["\nNewlines are respected only if its a single item on no indent!\n\nResult:"],
        {"columns": 2, "indent": 1}, prose_array])

    divider_function("Ending test 'printing_newlines'")

    pp([["Printing items in a 2 column adaptive layout"], {"indent": 1, "columns": 2, "column_width": 3, "filler": "."},
        _trash_list])
    pp([["Printing trash in a 3 column restrictive layout"],
        {"indent": 1, "columns": 3, "column_width": 5, "force_width": True, "filler": "-"}, _trash_list])
    pp([["Printing items in a narrow 5 column restrictive name-sorted layout"],
        {"key": lambda x: x, "indent": 1, "columns": 5, "column_width": 3, "force_width": True, "filler": "."},
        _trash_list])

    pp([["Length-sorting"], {"indent": 1, "columns": 1, "key": lambda x: len(x)}, _trash_list])
    pp([["Reverse-length-sorting"], {"indent": 1, "columns": 1, "key": lambda x: len(x), "reverse": True}, _trash_list])
    pp([["Unsorted single-column"], {"indent": 1, "columns": 1}, _trash_list])

    divider_function("Ending test 'printing and sorting'")


def inspector(r):
    divider_function("Beginning test 'inspector'")

    e = ECS.Entity(r)
    e.grant(ECS.Component(r, "color"))
    e.grant(ECS.Component(r, "position", 10, 15))
    e.grant(ECS.Component(r, "age"))
    # tools.inspect(e)
    tools.inspect(e.components["position"])
    divider_function("Ending test 'inspector'")


def ecs_systems(r):
    divider_function("Beginning test 'ecs_systems'")

    e = ECS.Entity(r)
    e.grant(ECS.Component(r, "color"))
    e.grant(ECS.Component(r, "position", 10, 15))
    e.grant(ECS.Component(r, "age"))

    def update_stamp(e):
        c_age = e.components["age"]
        c_age.updated = datetime.datetime.now()

    def print_diff(e):
        c_age = e.components["age"]
        diff = c_age.updated - c_age.created
        print(diff)

    ECS.System(r, "Time-Updater", "age", function_profile=[update_stamp, print_diff])

    for i in range(30):
        for j in r.systems:
            r.systems[j].update(r)

    divider_function("Ending test 'ecs_systems'")


def pygame_systems(r):
    divider_function("Starting test 'pygame_systems'")

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    background = background.convert()
    
    screen.blit(background, (0, 0))
    clock = pygame.time.Clock()
    mainloop = True
    FPS = 30
    playtime = 0.0

    e = ECS.Entity(r)
    e.grant(ECS.Component(r, "position", 50, 100))
    c = ECS.Component(r, "vector")
    c.x = 10
    c.y = 7
    e.grant(c)

    def apply_motion(e):
        e.components["position"].x += e.components["vector"].x
        e.components["position"].y += e.components["vector"].y
        print("{0:.2f},{1:.2f}".format(e.components["position"].x, e.components["position"].y))

    def correct_oob(e):
        maxx, maxy = screen.get_size()

        if e.components["position"].x < 0:
            e.components["vector"].x = -e.components["vector"].x
            e.components["position"].x = 0
        if e.components["position"].x > maxx:
            e.components["vector"].x = -e.components["vector"].x
            e.components["position"].x = maxx
        if e.components["position"].y < 0:
            e.components["vector"].y = -e.components["vector"].y
            e.components["position"].y = 0
        if e.components["position"].y > maxy:
            e.components["vector"].y = -e.components["vector"].y
            e.components["position"].y = maxy

    s = ECS.System(r, "Movement", "vector", "position", function_profile=[apply_motion, correct_oob])

    while mainloop:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
        r.update()
        # print("X: {} Y: {}".format(e.components["position"].x, e.components["position"].y))
        text = ":FPS: {0:.2f} Playtime: {1:.2f}".format(clock.get_fps(), playtime)
        pygame.display.set_caption(text)
        pygame.display.flip()

    pygame.quit()
    print("Game played for {0:.2f} seconds".format(playtime))
    divider_function("Ending test 'pygame_systems'")
