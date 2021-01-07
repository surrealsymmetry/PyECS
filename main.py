import ECS
import ECS_Inspector as tools
import ECS_tests as tests

    ###
    ### Testing ECS, pwint, inspector
    ###

r = ECS.Rack()

#tests.populate_manipulate(r)
#tests.blueprinting(r)
#tests.printing_and_sorting(r)
#tests.inspector(r)
tests.ecs_systems(r)