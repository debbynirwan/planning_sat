"""Encoder

Description:
    This module encodes Planning Problem to Propositional Formulas in CNF
    (Conjunctive Normal Form)

License:
    Copyright 2021 Debby Nirwan

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from .pddl_adapter import PlanningProblem
from enum import Enum
from itertools import combinations


class Operator(Enum):
    AND = 0,
    OR = 1,
    IMPLIES = 2


class Clause(object):

    def __init__(self, fluent=None):
        if fluent:
            self._clause = [fluent]
            self._single = True
        else:
            self._clause = []
            self._single = False

    def __repr__(self):
        return f"Clause object. {self._clause}"

    def __len__(self):
        return len(self._clause)

    def __getitem__(self, item):
        return self._clause[item]

    def __contains__(self, item):
        return True if item in self._clause else False

    def __eq__(self, other):
        if self._single == other.is_single and self._clause == other.clause:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def add(self, fluent, operator: Operator):
        if len(self._clause) == 0:
            self._single = True
        else:
            self._single = False
            self._clause.append(operator)
        self._clause.append(fluent)

        return self

    @property
    def clause(self):
        return self._clause

    @property
    def is_single(self):
        return self._single

    @property
    def empty(self):
        return self._clause == []


class PlanningProblemEncoder(object):

    def __init__(self, dom_file: str, problem_file: str, length=1):
        self._problem = PlanningProblem(dom_file, problem_file)
        self._length = length
        self._propositional_formulas = self._encode()

    def _encode(self):
        actions = self._problem.actions
        fluents = self._problem.fluents

        # 1. encode initial state
        init_state = list(self._problem.initial_state)
        init_state_clauses = []
        for fluent in list(fluents):
            if fluent not in init_state:
                fluent = ('not',) + fluent
            fluent = fluent + ('0',)
            init_state_clauses.append(Clause(fluent))

        # 2. encode goal state
        goal_state = list(self._problem.goal_state)
        goal_state_clauses = []
        for goal in goal_state:
            goal_state_clauses.append(Clause(goal + (str(self._length),)))

        enc_actions_clauses = []
        explanatory_frame_axioms = []
        complete_exclusion_axiom = []

        for step in range(self._length):
            # 3. encode actions
            for act in actions:
                if act.effect_pos.issubset(act.precondition_pos):
                    continue
                action_tuple = ('not', act, str(step))
                # preconditions
                for p in act.precondition_pos:
                    if 'adjacent' in p:
                        continue
                    action_clause = Clause(action_tuple)
                    p = p + (str(step),)
                    action_clause.add(p, Operator.OR)
                    enc_actions_clauses.append(action_clause)
                # positive effects
                for e in act.effect_pos:
                    e = e + (str(step + 1),)
                    action_clause = Clause(action_tuple)
                    action_clause.add(e, Operator.OR)
                    enc_actions_clauses.append(action_clause)
                # negative effects
                for e in act.effect_neg:
                    e = ('not',) + e + (str(step + 1),)
                    action_clause = Clause(action_tuple)
                    action_clause.add(e, Operator.OR)
                    enc_actions_clauses.append(action_clause)

            # 4. explanatory frame axioms
            for fluent in fluents:
                act_with_pos_effect = []
                act_with_neg_effect = []
                for act in actions:
                    if act.effect_pos.issubset(act.precondition_pos):
                        continue
                    if fluent in act.effect_pos:
                        act_with_pos_effect.append(act)
                    elif fluent in act.effect_neg:
                        act_with_neg_effect.append(act)
                if act_with_pos_effect:
                    a_pos = fluent + (str(step),)
                    b_pos = ('not',) + fluent + (str(step + 1),)
                    clause_pos = Clause(a_pos)
                    clause_pos.add(b_pos, Operator.OR)
                    for act in act_with_pos_effect:
                        c_pos = (act, str(step))
                        clause_pos.add(c_pos, Operator.OR)
                    explanatory_frame_axioms.append(clause_pos)
                if act_with_neg_effect:
                    a_neg = ('not',) + fluent + (str(step),)
                    b_neg = fluent + (str(step + 1),)
                    clause_neg = Clause(a_neg)
                    clause_neg.add(b_neg, Operator.OR)
                    for act in act_with_neg_effect:
                        c_neg = (act, str(step))
                        clause_neg.add(c_neg, Operator.OR)
                    explanatory_frame_axioms.append(clause_neg)

            # 5. complete exclusion axiom
            for action_pair in combinations(actions, 2):
                if action_pair[0].effect_pos.issubset(
                        action_pair[0].precondition_pos):
                    continue
                if action_pair[1].effect_pos.issubset(
                        action_pair[1].precondition_pos):
                    continue
                action0_tuple = ('not', action_pair[0], str(step))
                action1_tuple = ('not', action_pair[1], str(step))
                action_pair_clause = Clause(action0_tuple)
                action_pair_clause.add(action1_tuple, Operator.OR)
                complete_exclusion_axiom.append(action_pair_clause)

        proposition_formulas = init_state_clauses + goal_state_clauses + \
            enc_actions_clauses + explanatory_frame_axioms + \
            complete_exclusion_axiom

        return proposition_formulas

    @property
    def propositional_formulas(self):
        return self._propositional_formulas
