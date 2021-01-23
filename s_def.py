import PyG
import ECS_Inspector as tools



def nudge_timer(e):
    c = e.components["timer"]
    c.delta = PyG.clock.tick(60)
    c.total += (c.delta / 1000)




