"""
Simple rules based engine

https://dev.to/fractalis/how-to-write-a-basic-rule-engine-in-python-3eik

"""

from typing import Any

class Fact:
    def __init__(self, **kwargs: Any):
        self.__dict__.update(kwargs)

def fact_test():
    person_fact = Fact(name="John Brown",
                       age="35",
                       occuptation="Software Developer")

    person_fact.age # Returns 35
