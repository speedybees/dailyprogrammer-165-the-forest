from enum import Enum

class Direction(Enum):
    north = n = 1
    northeast = ne = 2
    east = e = 3
    southeast = se = 4
    south = s = 5
    southwest = sw = 6
    west = w = 7
    northwest = nw = 8

class Node(object):
    def __init__(self):
        self.entities = set()
        self.travel_directions = {}

    def add_travel_direction(self, direction, node):
        """Indicate what node is reached by traveling a direction"""
        self.travel_directions[direction] = node

    def add_entity(self, entity):
        self.entities.add(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def move_entity_to_node(self, entity, node):
        self.remove_entity(entity)
        node.add_entity(entity)
        entity.node = node

    def get_entities_of_type(self, entity_type):
        return set([entity for entity in self.entities if type(entity) == entity_type])

    def has(self, entity_type):
        return (len(self.get_entities_of_type(entity_type)) > 0)

    def short(self):
        """Get the short (one character ASCII) value to display for
        what's in this node."""
        if len(self.entities) == 0:
            return '.'
        elif len(self.entities) == 1:
            return iter(self.entities).next().short()
        else:
            return '*'


