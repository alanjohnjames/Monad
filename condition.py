"""
Rule Engine Decision

https://dev.to/fractalis/how-to-write-a-basic-rule-engine-in-python-3eik

"""

from fact import Fact

from typing import Callable, Any, Dict, List

class Condition:
    def __init__(self, name: str, evaluation_function: Callable[[Fact], bool]):
        self.name = name
        self.eval_func = evaluation_function

    def evaluate(self, fact: Fact) -> bool:
        return self.eval_func(fact)
