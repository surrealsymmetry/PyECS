import ECS
import ECS_tools as tools
import ECS_tests as tests

    ###
    ### Testing ECS
    ###

r = ECS.Rack()

tests.populate_manipulate(r)
tests.blueprinting(r)
tests.inspecting(r)
