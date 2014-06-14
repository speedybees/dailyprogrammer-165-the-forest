from entity import Entity
from lumberjack import Lumberjack

class Bear(Entity):
    def __init__(self, node):
        Entity.__init__(self, node, 5)

    def action(self):
        for lumberjack in self.node.get_entities_of_type(Lumberjack):
            self.maw_lumberjack(lumberjack)

    def maw_lumberjack(self, lumberjack):
        lumberjack.alive = False
        self.on_lumberjack_mawed(self, lumberjack)

    # This is a callback, so self won't be a Bear
    def on_lumberjack_mawed(self, bear, lumberjack):
        pass

    def can_move(self):
        return not self.node.has(Lumberjack)
