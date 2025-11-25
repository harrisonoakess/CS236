"""Interpreter for Datalog programs.

Provides an interpreter interface for interpreting Datalog
programs using relational algebra.
"""

from typing import Iterator

from project4.datalogprogram import DatalogProgram, Predicate, Rule
from project4.relation import Relation


class Interpreter:
    """Interpreter class for Datalog.

    Defines the interface, and a place for the implementation, for interpreting
    Datalog programs. The interpreter must be implemented using relational algebra,
    so new attributes must be added to track the named relations in the Datalog
    program during the lifetime of the interpreter.

    Attributes:
        datalog (DatalogProgram): The Datalog program to interpret.
    """

    __slots__ = ["datalog", "table_list"]

    def __init__(self, datalog: DatalogProgram) -> None:
        self.datalog = datalog
        self.table_list: dict[str, Relation] = {}

    def eval_schemes(self) -> None:
        """Evaluate the schemes in the Datalog program.

        Create, and store in the interpreter, a relation for each scheme
        in the Datalog program. The _name_ of the scheme must be stored
        separate from the relation since the `Relation` type has no name
        attribute.
        """
        for i in self.datalog.schemes:
            list1 = []
            for j in i.parameters:
                list1.append(j.value)
            self.table_list[i.name] = Relation(list1, set())

    def eval_facts(self) -> None:
        """Evaluate the facts in the Datalog program.

        Create, and store in the appropriate relation belonging to the
        interpreter, a tuple for each fact in the Datalog program.
        """

        for i in self.datalog.facts:
            if i.name in self.table_list:
                set1 = []
                for j in i.parameters:
                    set1.append(j.value)
                self.table_list[i.name].add_tuple(tuple(set1))

    def eval_queries(self) -> Iterator[tuple[Predicate, Relation]]:
        """Yield each query and resulting relation from evaluation."

        For each query in the Datalog program, evaluate the query to get a
        resulting relation that is the answer to the query, and then yield
        the resulting `(query, relation)` tuple.

        Returns:
            out (tuple[Predicate, Relation]): An iterator to a tuple where the
            first element is the predicate for the query and the second element
            is the relation for the answer.
        """
        for i in self.datalog.queries:  # first line
            if i.name in self.table_list:
                relation1: Relation = self.table_list[i.name]  # end of line 2
                index = 0
                id_dict = {}
            for j in i.parameters:
                if j.is_string():
                    relation1 = relation1.select_eq_lit(
                        relation1.header[index], j.value
                    )  # line 3

                if j.is_id():
                    if j.value not in id_dict:
                        id_dict[j.value] = index
                    else:
                        src = id_dict[j.value]
                        relation1 = relation1.select_eq_col(
                            relation1.header[src], relation1.header[index]
                        )  # line 4
                index += 1
            index_proj = 0
            list_project = []
            for j in i.parameters:
                index_project = 0
                if j.is_id():
                    list_project.append(relation1.header[index_proj])
                    index_project += 1
                index_proj += 1
            relation1 = relation1.project(list_project)
            list_rename = []
            for j in i.parameters:
                # index_rename = 0
                # dict_rename = {}

                if j.is_id():
                    # dict_rename[index_rename] = j.value
                    list_rename.append(j.value)
                # index_rename += 1
            relation1 = relation1.rename(list_rename)

            header_list = []
            for z in relation1.header:
                if z not in header_list:
                    header_list.append(z)

            relation1 = relation1.project(header_list)

            yield (i, relation1)

    def single_query(self, i: Predicate) -> Relation:
        if i.name in self.table_list:
            relation1: Relation = self.table_list[i.name]  # end of line 2
            index = 0
            id_dict = {}
        for j in i.parameters:
            if j.is_string():
                relation1 = relation1.select_eq_lit(
                    relation1.header[index], j.value
                )  # line 3

            if j.is_id():
                if j.value not in id_dict:
                    id_dict[j.value] = index
                else:
                    src = id_dict[j.value]
                    relation1 = relation1.select_eq_col(
                        relation1.header[src], relation1.header[index]
                    )  # line 4
            index += 1
        index_proj = 0
        list_project = []
        for j in i.parameters:
            index_project = 0
            if j.is_id():
                list_project.append(relation1.header[index_proj])
                index_project += 1
            index_proj += 1
        relation1 = relation1.project(list_project)
        list_rename = []
        for j in i.parameters:
            # index_rename = 0
            # dict_rename = {}

            if j.is_id():
                # dict_rename[index_rename] = j.value
                list_rename.append(j.value)
            # index_rename += 1
        relation1 = relation1.rename(list_rename)

        header_list = []
        for z in relation1.header:
            if z not in header_list:
                header_list.append(z)

        relation1 = relation1.project(header_list)

        return relation1

    def eval_rules(self) -> Iterator[tuple[Relation, Rule, Relation]]:
        """Yield each _before_ relation, rule, and _after_ relation from evaluation.

        For each rule in the Datalog program, yield as a tuple the relation associated
        with the rule before evaluating the rule one time, the rule itself, and then
        the resulting relation after evaluating the rule one time. This process
        should repeat until the associated relations stop changing.
        All the generated facts should be stored in the appropriate relation
        in the interpreter.

        For example, given `rule_a` for relation `A`, `rule_b` for
        relation `B`, and that it takes three evaluations to see no change, then
        `eval_rules` should:

            yield((A_0, rule_a, A_1))
            yield((B_0, rule_b, B_1))
            yield((A_1, rule_a, A_2))
            yield((B_1, rule_b, B_2))
            yield((A_2, rule_a, A_3))
            yield((B_2, rule_b, B_3))

        Here `A_0` is the initial relation for `A`, `A_1` is the relation after evaluating
        `rule_a` on `A_0` etc. The same for `B`. The iteration stops because `A_2 == A_3` and
        `B_2 == B_3`.

        Returns:
            out (Iterator[tuple[Relation, Rule, Relation]]): An iterator to a tuple where the
                first element is the relation before rule evaluation, the second element is
                the rule associated with the relation, and the third element is the relation
                resulting from the rule evaluation.
        """
        finish = True
        while finish:
            finish = False
            for rule in self.datalog.rules:  # this loops through each rule
                list_of_predicates = []
                for predicate in rule.predicates:  # This loops through the right side of the rule which is a list of predicates
                    list_of_predicates.append(self.single_query(predicate))
                combined_relation: Relation = list_of_predicates[0]
                list_of_predicates.pop(0)
                while len(list_of_predicates) > 0:
                    combined_relation = combined_relation.join(list_of_predicates[0])
                    list_of_predicates.pop(0)
                # There should be one relation now that is fully combined at this point
                header_list = []
                for head in rule.head.parameters:
                    if head.is_id():
                        if head not in header_list:
                            header_list.append(head.value)
                combined_relation = combined_relation.project(header_list)
                # There should be one relation that has completed projection at this point
                original_relation = self.table_list[rule.head.name]
                combined_relation = combined_relation.rename(original_relation.header)
                # There should be one relation that has a completed rename at this point
                combined_relation = combined_relation.union(original_relation)
                # This should complete the union up to this point
                if len(original_relation.set_of_tuples) != len(
                    combined_relation.set_of_tuples
                ):
                    finish = True
                yield (original_relation, rule, combined_relation)
                self.table_list[rule.head.name] = combined_relation

            # raise NotImplementedError

    def eval_rules_optimized(self) -> Iterator[tuple[Relation, Rule, Relation]]:
        """Yield each _before_ relation, rule, and _after_ relation from optimized evaluation.

        This function is the same as the `eval_rules` function only it groups rules by strongly
        connected components (SCC) in the dependency graph from the rules in the Datalog
        program. So given the first SCC is with `rule_a` for relation `A`, `rule_b` for
        relation `B`, that takes three evaluations to see no change, and the second SCC with
        `rule_c for relation C that takes two evaluations to see no change, then
        `eval_rules_opt` should:

            yield((A_0, rule_a, A_1))
            yield((B_0, rule_b, B_1))
            yield((A_1, rule_a, A_2))
            yield((B_1, rule_b, B_2))
            yield((A_2, rule_a, A_3))
            yield((B_2, rule_b, B_3))
            yield((C_0, rule_c, C_1))
            yield((C_1, rule_c, C_2))

        Here `A_0` is the initial relation for `A`, `A_1` is the relation after evaluating
        `rule_a` on `A_0` etc. The same for `B` and `C`. The iteration on the first SCC stops
        because `A_2 == A_3` and `B_2 == B_3`. After the iteration for the second SCC starts
        and stops after two iterations when `C_1 == C_2`.

        Returns:
            out (Iterator[tuple[Relation, Rule, Relation]]): An iterator to a tuple where the
                first element is the relation before rule evaluation, the second element is the
                rule associated with the relation, and the third element is the relation resulting
                from the rule evaluation.
        """
        raise NotImplementedError

    def get_rule_dependency_graph(self) -> dict[str, list[str]]:
        """Return the rule dependency graph.

        Computes and returns the graph formed by dependencies between rules.
        The graph is used to compute strongly connected components of rules
        for optimized rule evaluation.

        Rules are zero-indexed so the first rule in the Datalog program is `R0`,
        the second rules is `R1`, etc. A return of `{R0 : [R0, R1], R1 : [R2]}`
        means that `R0` has edges to `R0` and `R1`, and `R1` has an edge to `R2`.

        Returns:
            out: A map with an entry for each rule and the associated rules connected to it.
        """
        raise NotImplementedError
