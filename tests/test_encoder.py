from planning_sat.encoder import PlanningProblemEncoder, Clause, Operator
from pddlpy.pddl import Operator as Op


formulas = [Clause(('atl', 'rob', 'loc1', '0')),
            Clause(('not', 'atl', 'rob', 'loc2', '0')),
            Clause(('atl', 'rob', 'loc2', '1')),
            Clause((
                'not',
                Op('move', {'?r': 'rob', '?from': 'loc1', '?to': 'loc2'}),
                '0')).add(('atl', 'rob', 'loc1', '0'), Operator.OR),
            Clause((
                'not',
                Op('move', {'?r': 'rob', '?from': 'loc1', '?to': 'loc2'}),
                '0')).add(('atl', 'rob', 'loc2', '1'), Operator.OR),
            Clause((
                'not',
                Op('move', {'?r': 'rob', '?from': 'loc1', '?to': 'loc2'}),
                '0')).add(('not', 'atl', 'rob', 'loc1', '1'), Operator.OR),
            Clause((
                'not',
                Op('move', {'?r': 'rob', '?from': 'loc2', '?to': 'loc1'}),
                '0')).add(('atl', 'rob', 'loc2', '0'), Operator.OR),
            Clause((
                'not',
                Op('move', {'?r': 'rob', '?from': 'loc2', '?to': 'loc1'}),
                '0')).add(('atl', 'rob', 'loc1', '1'), Operator.OR),
            Clause((
                'not',
                Op('move', {'?r': 'rob', '?from': 'loc2', '?to': 'loc1'}),
                '0')).add(('not', 'atl', 'rob', 'loc2', '1'), Operator.OR),
            Clause(('atl', 'rob', 'loc1', '0')).add(
                ('not', 'atl', 'rob', 'loc1', '1'), Operator.OR).add(
                (Op('move', {'?r': 'rob', '?from': 'loc2', '?to': 'loc1'}), '0'
                 ), Operator.OR),
            Clause(('not', 'atl', 'rob', 'loc1', '0')).add(
                ('atl', 'rob', 'loc1', '1'), Operator.OR).add(
                (Op('move', {'?r': 'rob', '?from': 'loc1', '?to': 'loc2'}), '0'
                 ), Operator.OR),
            Clause(('atl', 'rob', 'loc2', '0')).add(
                ('not', 'atl', 'rob', 'loc2', '1'), Operator.OR).add(
                (Op('move', {'?r': 'rob', '?from': 'loc1', '?to': 'loc2'}), '0'
                 ), Operator.OR),
            Clause(('not', 'atl', 'rob', 'loc2', '0')).add(
                ('atl', 'rob', 'loc2', '1'), Operator.OR).add(
                (Op('move', {'?r': 'rob', '?from': 'loc2', '?to': 'loc1'}), '0'
                 ), Operator.OR),
            Clause(('not',
                    Op('move', {'?r': 'rob', '?from': 'loc1', '?to': 'loc2'}),
                    '0')).add(('not', Op('move', {'?r': 'rob', '?from': 'loc2',
                                                  '?to': 'loc1'}), '0'),
                              Operator.OR)
            ]


class TestEncoder:

    def test_encoder(self):
        encoded_pp = PlanningProblemEncoder("domain/simple-domain.pddl",
                                            "domain/simple-problem.pddl")
        pp = encoded_pp.propositional_formulas
        assert len(pp) == len(formulas)
