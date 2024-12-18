import pytest
from rules_engine.rules_engine_ecs import DataComponent, Entity, RuleSystem, World


@pytest.fixture
def world():
    return World()


def test_entity_creation():
    entity = Entity.create()
    assert entity.id == 0
    assert entity.components == {}


def test_add_component():
    entity = Entity.create()
    component = DataComponent(10)
    entity.add_component(component)
    assert DataComponent in entity.components
    assert entity.get_component(DataComponent) == component


def test_rule_system(world, capsys):
    entity = Entity.create()
    entity.add_component(DataComponent(12))
    world.add_entity(entity)

    def rule_condition(value): return value > 10
    def rule_action(entity): return print(
        f"Entity {entity.id}: Rule is satisfied.")
    rule_system = RuleSystem(rule_condition, rule_action)
    world.add_system(rule_system)

    world.process()
    captured = capsys.readouterr()
    assert "Entity 0: Rule is satisfied." in captured.out
    assert entity not in world.entities


def test_rule1(world, capsys):
    entity = Entity.create()
    entity.add_component(DataComponent(12))
    world.add_entity(entity)

    def rule_condition(value): return value > 10
    def rule_action(entity): return print(
        f"Entity {entity.id}: Rule 1 is satisfied.")
    world.add_system(RuleSystem(rule_condition, rule_action))

    world.process()
    captured = capsys.readouterr()
    assert "Entity 0: Rule 1 is satisfied." in captured.out
    assert entity not in world.entities


def test_rule2(world, capsys):
    entity = Entity.create()
    entity.add_component(DataComponent(8))
    world.add_entity(entity)

    def rule_condition(value): return value % 2 == 0

    def rule_action(entity): return print(
        f"Entity {entity.id}: Rule 2 is satisfied.")
    world.add_system(RuleSystem(rule_condition, rule_action))

    world.process()
    captured = capsys.readouterr()
    assert "Entity 0: Rule 2 is satisfied." in captured.out
    assert entity not in world.entities
