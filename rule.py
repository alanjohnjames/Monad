"""
Rule Engine Rule

https://dev.to/fractalis/how-to-write-a-basic-rule-engine-in-python-3eik

"""

from condition import Condition
from action import Action
from fact import Fact

from typing import Any, List
from functools import reduce

class Rule:
    def __init__(self, condition: Condition, action: Action):
        self.conditions = [condition]
        self.actions = [action]

    def add_condition(self, condition: Condition) -> None:
        self.conditions.append(condition)

    def add_action(self, action: Action) -> None:
        self.actions.append(action)

    def evaluate(self, facts: List[Fact]) -> Any:
        def fact_generator(conditions: List[Condition], facts: List[Fact]):
            all_conditions_true = True
            for fact in facts:
                results = map(lambda condition: condition.eval_func(fact), conditions)
                all_conditions_true = reduce(lambda x, y: x and y, results)

                if all_conditions_true:
                    yield fact

        true_facts = list(fact_generator(self.conditions, facts))

        if len(true_facts) > 0:
            for fact in true_facts:
                for action in self.actions:
                    action.exec_func(fact)
