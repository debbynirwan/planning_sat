"""Encoder

Description:
    This module runs DPLL (Davis–Putnam–Logemann–Loveland) Algorithm
    to solve satisfiability problem

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
from planning_sat.encoder import PlanningProblemEncoder, Operator, Clause
from typing import List, Set
import copy
import pddlpy
import time
import argparse
import os
import sys


class DPLL(object):

    def __call__(self, formulas: List[Clause], model=None):

        if len(formulas) == 0:
            return True, model

        if any([clause.empty for clause in formulas]):
            return False, None

        if not model:
            model = set()

        next_clause, unit = self._select_literal(formulas)

        if not unit or ('not' not in next_clause):
            positive_formulas = copy.deepcopy(formulas)
            positive_clause = self._pos_clause(next_clause)
            new_model, new_formulas = self._unit_propagation(positive_formulas,
                                                             model,
                                                             positive_clause)

            sat, new_model = self.__call__(new_formulas, new_model)
            if sat:
                return sat, new_model

        if not unit or ('not' in next_clause):
            negative_formulas = copy.deepcopy(formulas)
            negative_clause = self._neg_clause(next_clause)
            new_model, new_formulas = self._unit_propagation(negative_formulas,
                                                             model,
                                                             negative_clause)

            sat, new_model = self.__call__(new_formulas, new_model)
            if sat:
                return sat, new_model

        return False, None

    def _select_literal(self, formulas):
        if formulas == list():
            return None, None

        unit_clause = self._get_unit_clause(formulas)
        if unit_clause:
            return unit_clause, True

        return formulas[0].clause[0], False

    @staticmethod
    def _get_unit_clause(formulas):
        for clause in formulas:
            if clause.is_single:
                return clause.clause[0]
        return None

    @staticmethod
    def _unit_propagation(formulas: List[Clause], model: Set[Clause],
                          unit_clause):

        new_formulas = copy.deepcopy(formulas)
        model = model.union(unit_clause)
        # new_formulas.remove(unit_clause)

        if not new_formulas:
            return model, new_formulas

        if 'not' in unit_clause.clause[0]:
            reverse_clause = list(unit_clause.clause[0])
            reverse_clause.remove('not')
            not_unit_clause = Clause(tuple(reverse_clause))
        else:
            reverse_clause = ('not',) + unit_clause.clause[0]
            not_unit_clause = Clause(reverse_clause)

        for clause in list(new_formulas):
            for cl in clause.clause:
                if isinstance(cl, Operator):
                    continue
                if unit_clause.clause[0] == cl:
                    new_formulas.remove(clause)
                    break
                if not_unit_clause.clause[0] == cl:
                    new_formulas.remove(clause)
                    new_clause = Clause()
                    literals = []
                    for literal in clause:
                        if not isinstance(literal, Operator) and \
                                literal != not_unit_clause.clause[0]:
                            literals.append(literal)
                    if literals:
                        for literal in literals:
                            new_clause.add(literal, Operator.OR)
                    new_formulas.append(new_clause)
                    break

        return model, new_formulas

    @staticmethod
    def _pos_clause(atom: tuple):
        if 'not' in atom:
            pos_atom = list(atom)
            pos_atom.remove('not')
            pos_atom = tuple(pos_atom)
        else:
            pos_atom = atom

        return Clause(pos_atom)

    @staticmethod
    def _neg_clause(atom: tuple):
        if 'not' in atom:
            neg_atom = atom
        else:
            neg_atom = ('not',) + atom

        return Clause(neg_atom)

    @staticmethod
    def _pos_and_neg_atoms(atom: tuple):
        if 'not' in atom:
            neg_atom = atom
            pos_atom = list(atom)
            pos_atom.remove('not')
            pos_atom = tuple(pos_atom)
        else:
            pos_atom = atom
            neg_atom = ('not',) + atom

        return pos_atom, neg_atom


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Solving SAT Formulas using DPLL Algorithm",
        allow_abbrev=False
    )

    parser.add_argument(
        "-d", "--domain",
        required=True,
        type=str,
        help="path to pddl domain file"
    )

    parser.add_argument(
        "-p", "--problem",
        required=True,
        type=str,
        help="path to pddl problem file"
    )

    parser.add_argument(
        "-l", "--length",
        required=True,
        type=int,
        default=1,
        help="specify the length of steps in formulas encoding"
    )

    parser.add_argument(
        "-f", "--print",
        action='store_true',
        help="print the result"
    )

    return parser


if __name__ == "__main__":

    args = setup_parser().parse_args()
    if not os.path.isfile(args.domain) or not os.path.isfile(args.problem):
        sys.exit(1)

    domain_file = args.domain
    problem_file = args.problem
    length = args.length
    print_debug = args.print

    pp_encoder = PlanningProblemEncoder(domain_file, problem_file, length)

    dpll = DPLL()

    if print_debug:
        print(f"DPLL algorithm running with "
              f"{len(pp_encoder.propositional_formulas)} formulas")
    start_time = time.perf_counter()
    result_dp, final_model = dpll(pp_encoder.propositional_formulas)
    end_time = time.perf_counter()
    if print_debug:
        print(f"DPLL algorithm ran for {end_time-start_time:0.4f} seconds")
        if result_dp:
            print("Plan:")
            operator_list = []
            for item in final_model:
                if 'not' not in item and isinstance(item[0], pddlpy.Operator):
                    operator_list.append(item)
            operator_list.sort(key=lambda tup: tup[-1])
            for op in operator_list:
                print(op)
        else:
            print(f"Failed to plan at length {length}")
