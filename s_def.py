import rack
import random
import PyG
import pygame
import ECS_Inspector as tools

overlay_color_mint = (180, 255, 200)
overlay_color_bubblegum = (255, 180, 200)
lineweight = 3
sprite_surface = pygame.Surface((lineweight, lineweight))
sprite_surface.fill(overlay_color_bubblegum)
__atlas = {("point"):sprite_surface} # used by prep_sprites and render


def pygame_global_timer(e):
    c = e.components["pygame_global_timer"]
    c.delta = PyG.clock.tick_busy_loop(60)
    c.total += (c.delta / 1000)

def timer_countdown(e):
    assert "timer_countdown" in e.components, "{}".format(e.components.keys())
    c = e.components["timer_countdown"]
    c.remaining -= (PyG.e_timer.components["pygame_global_timer"].delta / 1000)

def point_dot_source(e):
    c_source = e.components["particle_source"]
    c_spawn_timer = e.components["timer_countdown"]
    source_x, source_y = e.components["position"].x, e.components["position"].y
    particle_lifespan = 4
    #define a particle
    def spawn_point_dot(lifespan):
        # this is stupid
        # producing a normalized vector in a random float radian circle direction would be correct
        # i dont have that tech yet
        def generate_direction():
            dx = random.uniform(2, 3)
            dy = random.uniform(0, 3)
            #print("1: {} {}".format(dx, dy))

            #equal chance of left/right/up/down
            if random.choice([True, False]):
                dx *= -1
            if random.choice([True, False]):
                dy *= -1
            #print("2: {} {}".format(dx, dy))
            #equal chance for either axis to be the "definitely moving" axis
            if random.choice([True, False]):
                temp = dx
                dx = dy
                dy = temp
            #print("3: {} {}".format(dx, dy))
            return dx, dy

        e_particle = rack.e()
        e_particle.grant(rack.c("particle", e.id))
        e_particle.grant(rack.c("sprite"))
        e_particle.grant(rack.c("position", source_x, source_y))
        e_particle.grant(rack.c("momentum", *generate_direction()))
        e_particle.grant(rack.c("timer_countdown", lifespan))
        return e_particle

    def particle_behaviour(p):
        p.components["position"].x += p.components["momentum"].x
        p.components["position"].y += p.components["momentum"].y

    #make a new particle sometimes

    if c_spawn_timer.remaining <= 0:
        c_spawn_timer.remaining = c_source.rate
        #either we're under the particle cap or there is no cap
        if len(c_source.particles) < c_source.max - 1 or c_source.max <= 0:
            c_source.particles.append(spawn_point_dot(particle_lifespan))

    #update all particles positions every time
    for i in range(0, len(c_source.particles)-1):
        ###
        ### this line throws an error when exiting pygame loop sometimes?
        ### list index out of range
        ### it should be in range by definition at this point i dont get it
        ### todo add a more descriptive throw
        p = c_source.particles[i]
        c_particle_lifespan = p.components["timer_countdown"]
        if c_particle_lifespan.remaining <= 0:
            c_source.particles.pop(i)
            p.purge(p)
        else:
            particle_behaviour(p)

            
def render(e):
    c = e.components["sprite"]
    pos = e.components["position"].x, e.components["position"].y
    curr_sprite = None
    if hasattr(c, 'sprite'):
        curr_sprite = __atlas[c.sprite]
    elif hasattr(c, 'box'):
        curr_sprite = __atlas[c.box]
    elif hasattr(c, 'point'):
        curr_sprite = __atlas[c.point]
    else:
        if "box" in e.components:
            # box entity
            atlas_key = ("box", e.components["box"].x, e.components["box"].y)
            width, height = atlas_key[1], atlas_key[2]
            if atlas_key not in __atlas:
                sprite_surface = pygame.Surface((width, height))
                sprite_surface.set_colorkey((0, 0, 0))
                pygame.draw.rect(sprite_surface, overlay_color_mint, (0, 0, width, height), width=lineweight)
                __atlas[atlas_key] = sprite_surface.convert_alpha()
            e.components["sprite"].box = ("box", width, height)
            curr_sprite = __atlas[atlas_key]
            #print("\tbox entity prepped for ", e.id)
        else:
            # point entity
            e.components["sprite"].point = ("point")
            curr_sprite = __atlas[("point")]
            #print("\tpoint entity prepped for ", e.id)

    PyG.screen.blit(curr_sprite, pos)


