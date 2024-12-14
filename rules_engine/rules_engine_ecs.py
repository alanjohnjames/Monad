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

class Rule1System:
    def process(self, entities):
        for entity in entities:
            data = entity.get_component(DataComponent)
            if data and data.value > 10:
                print(f"Entity {entity.id}: Rule1 is satisfied.")
                entities.remove(entity)

class Rule2System:
    def process(self, entities):
        for entity in entities:
            data = entity.get_component(DataComponent)
            if data and data.value % 2 == 0:
                print(f"Entity {entity.id}: Rule2 is satisfied.")
                entities.remove(entity)

class Rule3System:
    def process(self, entities):
        for entity in entities:
            data = entity.get_component(DataComponent)
            if data and data.value % 5 == 0:
                print(f"Entity {entity.id}: Rule3 is satisfied.")
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

    world.add_system(Rule1System())
    world.add_system(Rule2System())
    world.add_system(Rule3System())

    world.process()
