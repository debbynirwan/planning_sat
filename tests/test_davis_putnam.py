from planning_sat.davis_putnam import DavisPutnam
from planning_sat.encoder import Clause, Operator


model = {('not', 'B'), ('not', 'A'), ('D',)}


class TestDPLL:

    def test_dpll(self):
        forms = []
        clause_1 = Clause(('D',))
        forms.append(clause_1)
        clause_2 = Clause(('not', 'D'))
        clause_2.add(('A',), Operator.OR)
        clause_2.add(('not', 'B'), Operator.OR)
        forms.append(clause_2)
        clause_3 = Clause(('not', 'D'))
        clause_3.add(('not', 'A'), Operator.OR)
        clause_3.add(('not', 'B'), Operator.OR)
        forms.append(clause_3)
        clause_4 = Clause(('not', 'D'))
        clause_4.add(('not', 'A'), Operator.OR)
        clause_4.add(('B',), Operator.OR)
        forms.append(clause_4)
        clause_5 = Clause(('D',))
        clause_5.add(('A',), Operator.OR)
        forms.append(clause_5)

        davis_putnam = DavisPutnam()
        result_dp, final_model = davis_putnam(forms)

        assert result_dp
        assert final_model == model
