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

class RuleSystem:
    def __init__(self, condition):
        self.condition = condition

    def process(self, entities):
        for entity in entities:
            data = entity.get_component(DataComponent)
            if data and self.condition(data.value):
                print(f"Entity {entity.id}: Rule is satisfied.")
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
            system.process(self.entities)

if __name__ == "__main__":

    world = World()

    entity = Entity()
    entity.add_component(DataComponent(12))
    world.add_entity(entity)

    rule1_condition = lambda value: value > 10
    rule2_condition = lambda value: value % 2 == 0
    rule3_condition = lambda value: value % 5 == 0

    world.add_system(RuleSystem(rule1_condition))
    world.add_system(RuleSystem(rule2_condition))
    world.add_system(RuleSystem(rule3_condition))

    world.process()
