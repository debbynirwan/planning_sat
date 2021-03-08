from planning_sat.pddl_adapter import PlanningProblem
from pddlpy.pddl import Operator


initial_state = [("adjacent", "loc1", "loc2"),
                 ("adjacent", "loc2", "loc1"),
                 ("in", "conta", "loc1"),
                 ("in", "contb", "loc2"),
                 ("atl", "robr", "loc1"),
                 ("atl", "robq", "loc2"),
                 ("unloaded", "robr"),
                 ("unloaded", "robq")]

goal_state = [("in", "contb", "loc1"),
              ("in", "conta", "loc2")]

fluents = [('atl', 'robr', 'loc1'),
           ('atl', 'robr', 'loc2'),
           ('atl', 'robq', 'loc1'),
           ('atl', 'robq', 'loc2'),
           ('loaded', 'robr', 'conta'),
           ('loaded', 'robr', 'contb'),
           ('loaded', 'robq', 'conta'),
           ('loaded', 'robq', 'contb'),
           ('unloaded', 'robr'),
           ('unloaded', 'robq'),
           ('in', 'conta', 'loc1'),
           ('in', 'conta', 'loc2'),
           ('in', 'contb', 'loc1'),
           ('in', 'contb', 'loc2')]


class TestPlanningProblem:

    def test_constructor(self):
        pp = PlanningProblem("domain/dock-worker-robot-domain.pddl",
                             "domain/dock-worker-robot-problem.pddl")

        assert type(pp.initial_state) is set
        assert type(pp.goal_state) is set
        assert type(pp.actions) is list
        assert type(pp.fluents) is list

    def test_initial_state(self):
        pp = PlanningProblem("domain/dock-worker-robot-domain.pddl",
                             "domain/dock-worker-robot-problem.pddl")
        assert pp.initial_state == set(initial_state)

    def test_goal_state(self):
        pp = PlanningProblem("domain/dock-worker-robot-domain.pddl",
                             "domain/dock-worker-robot-problem.pddl")
        assert pp.goal_state == set(goal_state)

    def test_actions(self):
        pp = PlanningProblem("domain/dock-worker-robot-domain.pddl",
                             "domain/dock-worker-robot-problem.pddl")
        for act in pp.actions:
            assert type(act) is Operator

    def test_fluents(self):
        pp = PlanningProblem("domain/dock-worker-robot-domain.pddl",
                             "domain/dock-worker-robot-problem.pddl")
        assert set(pp.fluents) == set(fluents)
