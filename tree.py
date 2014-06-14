from entity import Entity
from enum import Enum
from sys import maxint
import random

class TreeType(object):
    def __init__(self, representation, long_name, max_age, spawn_probability, harvestable_wood, next_type):
        self.representation = representation
        self.long_name = long_name
        self.max_age = max_age
        self.spawn_probability = spawn_probability
        self.harvestable_wood = harvestable_wood
        self.next_type = next_type

    def short(self):
        return self.representation

class Tree(Entity):
    elder_tree = TreeType('E', 'Elder Tree', maxint, 0.2, 2, None)
    normal = TreeType('T', 'Tree', 120, 0.1, 1, elder_tree)
    sapling = TreeType('S', 'Sapling', 12, 0, 0, normal)

    def __init__(self, node, age=12, tree_type=normal):
        Entity.__init__(self, node, 0)
        self.age = age
        self.tree_type = tree_type

    def __getattribute__(self, name):
        if name == 'harvestable_wood':
            return self.tree_type.harvestable_wood
        else:
            return object.__getattribute__(self, name)

    def on_spawn(self, new_tree):
        pass

    def on_change_tree_type(self, old_type, new_type):
        pass

    def short(self):
        return self.tree_type.short()

    def action(self):
        if (random.random() <= self.tree_type.spawn_probability):
            self.spawn_tree()
        self.increase_age()

    def increase_age(self, increase_amount=1):
        self.age += increase_amount
        if (self.age >= self.tree_type.max_age):
            self.on_change_tree_type(self, self.tree_type, self.tree_type.next_type)
            self.tree_type = self.tree_type.next_type

    def harvest(self):
        """Kill the tree and return how much wood was harvested"""
        self.alive = False
        return self.harvestable_wood

    def spawn_tree(self):
        # Saplings can't spawn; of course we shouldn't be in here in the 
        # first place
        if self.tree_type != Tree.sapling and self.node is not None:
            # Ignore any nodes which contain trees
            adjacent_tree_free_nodes = [node for node in self.node.travel_directions.values() 
                                        if not node.has(Tree)]
            if (len(adjacent_tree_free_nodes) > 0):
                target_node = random.choice(adjacent_tree_free_nodes)
                new_tree = Tree(target_node, 0, Tree.sapling)
                target_node.add_entity(new_tree)
                self.on_spawn(new_tree)
                new_tree.on_spawn = self.on_spawn
                new_tree.on_change_tree_type = self.on_change_tree_type
                 

