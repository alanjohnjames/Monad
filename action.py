"""
Rule Engine Action

https://dev.to/fractalis/how-to-write-a-basic-rule-engine-in-python-3eik

"""

from typing import Callable, Any, Dict, List
from fact import Fact

class Action:

    def __init__(self, name: str, execution_function: Callable[[Fact], None]):
        self.name = name
        self.exec_func = execution_function

    def execute(self, fact: Fact) -> None:
        self.exec_func(fact)
