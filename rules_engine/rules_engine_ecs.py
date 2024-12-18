"""
Implementing a Waterfall of Business Rules in Python using the ECS pattern.

"""

class DataComponent:
    def __init__(self, value):
        self.value = value

class Entity:
    _id_counter = 0

    def __init__(self):
        self.id = Entity._id_counter
        Entity._id_counter += 1
        self.components = {}

    def add_component(self, component):
        self.components[type(component)] = component

    def get_component(self, component_type):
        return self.components.get(component_type)

class ConditionSystem:
    def __init__(self, condition):
        self.condition = condition
        self.satisfied_entities = []

    def process(self, entities):
        self.satisfied_entities = []
        for entity in entities:
            data = entity.get_component(DataComponent)
            if data and self.condition(data.value):
                self.satisfied_entities.append(entity)

class ActionSystem:
    def __init__(self, action):
        self.action = action

    def process(self, entities, satisfied_entities):
        for entity in satisfied_entities:
            self.action(entity)
            entities.remove(entity)

class World:
    def __init__(self):
        self.entities = []
        self.systems = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_system(self, system):
        self.systems.append(system)

    def process(self):
        for system in self.systems:
            if isinstance(system, ConditionSystem):
                system.process(self.entities)
            elif isinstance(system, ActionSystem):
                system.process(self.entities, system.satisfied_entities)

if __name__ == "__main__":

    world = World()

    entity = Entity()
    entity.add_component(DataComponent(12))
    world.add_entity(entity)

    rule1_condition = lambda value: value > 10
    rule2_condition = lambda value: value % 2 == 0
    rule3_condition = lambda value: value % 5 == 0

    rule1_action = lambda entity: print(f"Entity {entity.id}: Rule 1 is satisfied.")
    rule2_action = lambda entity: print(f"Entity {entity.id}: Rule 2 is satisfied.")
    rule3_action = lambda entity: print(f"Entity {entity.id}: Rule 3 is satisfied.")

    condition_system1 = ConditionSystem(rule1_condition)
    condition_system2 = ConditionSystem(rule2_condition)
    condition_system3 = ConditionSystem(rule3_condition)

    action_system1 = ActionSystem(rule1_action)
    action_system2 = ActionSystem(rule2_action)
    action_system3 = ActionSystem(rule3_action)

    world.add_system(condition_system1)
    world.add_system(condition_system2)
    world.add_system(condition_system3)
    world.add_system(action_system1)
    world.add_system(action_system2)
    world.add_system(action_system3)

    world.process()
