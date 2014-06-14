from entity import Entity
from tree import Tree

class Lumberjack(Entity):
    def __init__(self, node):
        Entity.__init__(self, node, 3)

    def action(self):
        lumber_collected = sum([tree.harvest() for tree in self.node.get_entities_of_type(Tree) if tree.tree_type != Tree.sapling])
        if lumber_collected > 0:
            self.on_lumber_collected(self, lumber_collected)

    # This is a callback, so self won't necessarily be a Lumberjack
    def on_lumber_collected(self, lumberjack, quantity):
        pass

    def can_move(self):
        return (len([tree for tree in self.node.get_entities_of_type(Tree) if tree.tree_type != Tree.sapling]) == 0)
