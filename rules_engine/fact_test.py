"""
Simple Rules Engine

https://dev.to/fractalis/how-to-write-a-basic-rule-engine-in-python-3eik

"""

from rules_engine.rules import Fact


def test_fact():
    person_fact = Fact(name="John Brown",
                    age="35",
                    occuptation="Software Developer")

    assert person_fact.age == '35'


if __name__ == '__main__':

    test_fact()

    print('Finished.')
