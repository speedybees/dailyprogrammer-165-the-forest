import random

class Entity(object):
    def __init__(self, node, max_moves):
        self.node = node
        self.alive = True
        self.max_moves = max_moves

    def action(self):
        """What to do after movement"""
        pass

    def can_move(self):
        """Whether there's anything interesting enough in this node to justify 
        stopping"""
        return True

    def move(self):
        """Move/Wander to a new node."""
        for i in xrange(self.max_moves):
            if self.can_move():
                retries = 1
                # Bears don't go where bears are, lumberjacks don't go where lumberjacks are
                # If that's where we're headed, retry
                while (retries >= 0):
                    random_adjacent_node = random.choice(self.node.travel_directions.values())
                    if not random_adjacent_node.has(type(self)):
                        self.node.move_entity_to_node(self, random_adjacent_node)
                        break
                    retries = retries - 1
                if retries == 0:
                # Stop moving if there don't seem to be enough places to move
                    break

    def short(self):
        return type(self).__name__[0]
