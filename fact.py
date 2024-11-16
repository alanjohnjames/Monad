#!python
"""
Simple Rules Engine

https://dev.to/fractalis/how-to-write-a-basic-rule-engine-in-python-3eik

"""

from typing import Any

class Fact:
    def __init__(self, **kwargs: Any):
        self.__dict__.update(kwargs)

