#!python3

# Main

from fact import Fact
from condition import Condition
from action import Action
from rule import Rule

age_cond = Condition(name="Age>=21",
                     evaluation_function=lambda fact: fact.age >= 21)
occupation_cond = Condition(name="Occupation==Software Developer",
                            evaluation_function=lambda fact: fact.occupation == "Software Developer")

print_action = Action(name="Print Fact",
                      execution_function=lambda fact: print(f"Name: {fact.name}"
                                                            f"Age: {fact.age}"
                                                            f"Occupation: {fact.occupation}"))

john = Fact(age=25,name="John Brown", occupation="Software Developer")
sarah = Fact(age=35,name="Sarah Purple", occupation="Data Engineer")
barry = Fact(age=27, name="Barry White", occupation="Software Developer")

rule = Rule(condition=age_cond, action=print_action)
rule.add_condition(occupation_cond)

rule.evaluate([john, sarah, barry])
