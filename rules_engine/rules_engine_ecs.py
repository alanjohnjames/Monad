"""
Implementing a Waterfall of Business Rules in Python using the ECS pattern.

"""
from typing import NamedTuple, Callable, Dict, List

class DataComponent(NamedTuple):
    value: int

class Entity(NamedTuple):
    id: int
    components: Dict[type, NamedTuple]

    _id_counter = 0

    @classmethod
    def create(cls):
        entity = cls(cls._id_counter, {})
        cls._id_counter += 1
        return entity

    def add_component(self, component: NamedTuple):
        self.components[type(component)] = component

    def get_component(self, component_type: type) -> NamedTuple:
        return self.components.get(component_type)

class RuleSystem(NamedTuple):
    condition: Callable[[int], bool]
    action: Callable[[Entity], None]

    def process(self, entities: List[Entity]):
        for entity in entities:
            data = entity.get_component(DataComponent)
            if data and self.condition(data.value):
                self.action(entity)
                if entity in entities:
                    entities.remove(entity)

class World(NamedTuple):
    entities: List[Entity] = []
    systems: List[NamedTuple] = []

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def add_system(self, system: NamedTuple):
        self.systems.append(system)

    def process(self):
        for system in self.systems:
            system.process(self.entities)

if __name__ == "__main__":
    world = World()

    entity = Entity.create()
    entity.add_component(DataComponent(12))
    world.add_entity(entity)

    rule1_condition = lambda value: value > 10
    rule2_condition = lambda value: value % 2 == 0
    rule3_condition = lambda value: value % 5 == 0

    rule1_action = lambda entity: print(f"Entity {entity.id}: Rule 1 is satisfied.")
    rule2_action = lambda entity: print(f"Entity {entity.id}: Rule 2 is satisfied.")
    rule3_action = lambda entity: print(f"Entity {entity.id}: Rule 3 is satisfied.")

    world.add_system(RuleSystem(rule1_condition, rule1_action))
    world.add_system(RuleSystem(rule2_condition, rule2_action))
    world.add_system(RuleSystem(rule3_condition, rule3_action))

    world.process()
