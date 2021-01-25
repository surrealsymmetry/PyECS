import rack
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


def blueprinting():
    divider_function("Beginning test 'blueprinting'")

    def spawn_one():
        e = rack.e()
        c = rack.c("position")
        c.x = 3
        e.grant(c)

        return e

    e = spawn_one()

    tools.inspect(e)
    print("\t Entity is at X: {} Y:{}".format(e.components["position"].x, e.components["position"].y))

    e_2 = spawn_one()
    e_2.grant(rack.c("color"))

    tools.inspect(e_2)
    tools.inspect(e_2.components["color"])

    print("\nColour 'Hot'\n\tRED:\t{}\n\tGREEN:\t{}\n\tBLUE:\t{}".format(
        e_2.components["color"].colors["hot"][0],
        e_2.components["color"].colors["hot"][1],
        e_2.components["color"].colors["hot"][2]))
    divider_function("Ending test 'blueprinting'")


def printing_and_sorting():
    divider_function("Starting test 'printing and sorting'")
    f_nam = ["becky", "noah", "bri", "jasper", "colin", "sandra", "peppin", "eleanor", "chester", "angelina", "grint",
             "oswald", "fiona", "parker", "trisha", "joanne", "serena"]
    l_nam = ["dreck", "berd", "auren", "suarez", "peach", "duard", "nona", "poleck", "merino", "grant", "chi", "decker",
             "wolf", "khan", "smith", "durent", "blunt", "parcey"]
    for i in range(len(f_nam)):
        for j in range(len(l_nam)):
            c = rack.c("name")  # doc=[["Component Spawning:"]])
            c.name = "{} {}".format(f_nam[i], l_nam[j])
            e = rack.e()  # doc=[["Entity Spawning:"]])
            e.grant(c)
            # print("{}\t{} {}".format(e.id, e.components["name"].name[0], e.components["name"].name[1]))

    print("{} entities spawned".format(len(rack.entities)))

    list = []
    for key in rack.entities:
        e = rack.entities[key]
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


def inspector():
    divider_function("Beginning test 'inspector'")

    e = rack.e()
    e.grant(rack.c("color"))
    e.grant(rack.c("position", 10, 15))
    tools.inspect(e)
    tools.inspect(e.components["position"])
    divider_function("Ending test 'inspector'")


def ecs_systems():
    divider_function("Beginning test 'ecs_systems'")

    e = rack.e()
    e.grant(rack.c("color"))
    e.grant(rack.c("position", 10, 15))

    c = rack.c("custom_age")
    c.created = datetime.datetime.now()
    print("#######", c.created)
    e.grant(c)

    def update_stamp(e):
        e.components["custom_age"].updated = datetime.datetime.now()

    def print_diff(e):
        c = e.components["custom_age"]
        diff = c.updated - c.created
        print(diff)

    s = rack.s("Time-Updater", "custom_age", update_stamp, print_diff)

    for i in range(300):
        s.update(rack)

    divider_function("Ending test 'ecs_systems'")


def pygame_systems():
    divider_function("Starting test 'pygame_systems'")

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    background = pygame.Surface(screen.get_size())
    background.fill((135, 95, 128))
    background = background.convert()

    screen.blit(background, (0, 0))
    clock = pygame.time.Clock()
    mainloop = True

    e = rack.e()
    e.grant(rack.c("position", 50, 100))
    c = rack.c("custom_vector")
    c.x,c.y = screen.get_size()
    e.grant(c)

    c = rack.c("custom_graphic")
    circle_radius = 20
    c.sprite = pygame.Surface((circle_radius * 2, circle_radius * 2))
    pygame.draw.circle(c.sprite, (255, 190, 235), (circle_radius, circle_radius), circle_radius)

    c.sprite = c.sprite.convert_alpha()
    e.grant(c)

    c = rack.c("custom_bounds")
    c.rect = e.components["custom_graphic"].sprite.get_rect()
    e.grant(c)

    e_timer = rack.e()
    c_timer = e_timer.grant(rack.c("custom_timer"))

    def nudge_timer(e):
        c = e.components["custom_timer"]
        if not hasattr(c, 'delta'):
            print("timer delta initialized")
            c.delta = 0
        if not hasattr(c, 'total'):
            c.total = 0
            print("timer total initialized")
        c.delta = clock.tick(60)    # hard coded fps
        c.total += (c.delta / 1000)

    def apply_motion(e):
        c = None
        for key in rack.components["custom_timer"]:        #this is really wack, im iterating over the list to grab a single unique item because i dont know the key?
            c = rack.components["custom_timer"].get(key)
        delta_ms = c.delta
        e.components["position"].x += delta_ms/1000 * e.components["custom_vector"].x
        e.components["position"].y += delta_ms/1000 * e.components["custom_vector"].y

    def correct_oob(e):
        pos = (e.components["position"].x, e.components["position"].y)
        x,y = pos
        maxx, maxy = screen.get_size()
        maxx -= e.components["custom_bounds"].rect[2]
        maxy -= e.components["custom_bounds"].rect[3]

        def flip_x(e):
            e.components["custom_vector"].x *= -1
            print("bink")
        def flip_y(e):
            e.components["custom_vector"].y *= -1
            print("bonk")

        if x < 0:
            flip_x(e)
            e.components["position"].x = 0
        if x > maxx:
            flip_x(e)
            e.components["position"].x = maxx
        if y < 0:
            flip_y(e)
            e.components["position"].y = 0
        if y > maxy:
            flip_y(e)
            e.components["position"].y = maxy


    def draw_thing(e):
        #tools.inspect(e)
        sprite = e.components["custom_graphic"].sprite
        pos = (e.components["position"].x, e.components["position"].y)
        screen.blit(sprite, pos)


    rack.s("Game Timer System", "custom_timer", nudge_timer)
    rack.s("Movement System", "custom_vector", "custom_bounds", "position", apply_motion, correct_oob)
    rack.s("Render System", "position", "custom_graphic", draw_thing)

    for key in rack.systems:
        tools.inspect(rack.systems[key])

    while mainloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
        screen.blit(background, (0,0))
        rack.update()
        if c_timer.total > 4:
            mainloop = False
        # print("X: {} Y: {}".format(e.components["position"].x, e.components["position"].y))
        text = ":FPS: {0:.2f} Playtime: {1:.2f}".format(clock.get_fps(), c_timer.total)
        pygame.display.set_caption(text)
        pygame.display.flip()

    pygame.quit()
    print("Game played for {0:.2f} seconds".format(c_timer.total))
    divider_function("Ending test 'pygame_systems'")
