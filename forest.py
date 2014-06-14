#! /usr/bin/python

from bear import Bear
from curses_view import CursesView
from lumberjack import Lumberjack
from node import Direction, Node
from record import Record
from statistics import StatisticsBatch
from tree import Tree
import argparse, curses, random
from time import sleep

class Forest(object):
    def __init__(self, width, height, population_proportions):
        self.width = width
        self.height = height
        self.initial_proportions = population_proportions
        self.current_tick = 1
        self.pending_entities = set()
        self.population = {Bear: set(), Lumberjack: set(), Tree: set()}
        self.layout = []

    def initialize(self):
        # This will be addressed as layout[width_coordinate][height_coordinate]
        self.layout = [[Node() for y in xrange(self.height)] for x in xrange(self.width)]
        self.statistics = StatisticsBatch()
        self.statistics.add_groups('month', 'year', 'all time')
        self.record = Record()
        self.current_tick = 1
        x = 0
        for row in self.layout:
            y = 0
            for node in row:
                self.add_connections(node, x, y)
                y += 1
            x += 1
        self.populate_forest()

    def add_connections(self, node, x, y):
        for direction in Direction:
            if direction in [Direction.northwest, Direction.north, Direction.northeast]:
                target_y = y + 1
            elif direction in [Direction.southwest, Direction.south, Direction.southeast]:
                target_y = y - 1
            else:
                target_y = y
            if direction in [Direction.northwest, Direction.west, Direction.southwest]:
                target_x = x + 1
            elif direction in [Direction.northeast, Direction.east, Direction.southeast]:
                target_x = x - 1
            else:
                target_x = x
            if (0 <= target_x < self.width) and (0 <= target_y < self.height):
                node.add_travel_direction(direction, self.layout[target_x][target_y])

    def get_all_nodes(self):
        return [node for row in self.layout for node in row]

    def populate_forest(self):
        self.all_entities = set()
        all_nodes = self.get_all_nodes()
        for entity_type in [Bear, Lumberjack, Tree]:
            self.spawn_entities(
                entity_type, 
                all_nodes, 
                int(self.initial_proportions[entity_type] * len(all_nodes)))

    def spawn_entities(self, entity_type, candidate_nodes, quantity):
        random.shuffle(candidate_nodes)
        to_return = set()
        for i in xrange(quantity):
            if i >= len(candidate_nodes):
                break
            entity = entity_type(candidate_nodes[i])
            self.set_callbacks(entity)
            self.add_entity(entity)
            candidate_nodes[i].add_entity(entity)
            to_return.add(entity)
        return to_return

    def set_callbacks(self, entity):
        if (type(entity) == Bear):
            entity.on_lumberjack_mawed = self.on_lumberjack_mawed
        elif (type(entity) == Lumberjack):
            entity.on_lumber_collected = self.on_lumber_collected
        elif (type(entity) == Tree):
            entity.on_spawn = self.on_spawned_tree
            entity.on_change_tree_type = self.on_change_tree_type

    def add_entity(self, entity):
        self.all_entities.add(entity)
        self.population[type(entity)].add(entity)

    def add_pending_entity(self, entity):
        """Since we'll be adding entities during a list comprehension,
        we need to store those new entities somewhere briefly."""
        self.pending_entities.add(entity)

    def on_change_tree_type(self, tree, old_type, new_type):
        self.statistics.log_all(old_type.long_name + " became " + new_type.long_name, 1)

    def on_lumber_collected(self, lumberjack, quantity): 
        self.statistics.log_all('lumber collected', quantity)

    def on_lumberjack_mawed(self, bear, lumberjack):
        self.statistics.log_all('lumberjacks mawed', 1)

    def on_spawned_tree(self, tree):
        self.add_pending_entity(tree)
        self.statistics.log_all("new Saplings created", 1)

    def kill_random_entity(self, entity_type):
        if len(self.population[entity_type]) > 0:
            for entity in random.sample([entity for entity in self.population[entity_type] if entity.alive], 1):
                entity.alive = False

    def get_total_of_entity(self, entity_type):
        return len([entity for entity in self.population[entity_type] if entity.alive])

    def tick(self):
        self.statistics['month'].clear()
        # Lumberjacks should move before bears so that bears stop where 
        # lumberjacks have stopped
        [[entity.move() for entity in self.population[entity_type]] for entity_type in [Lumberjack, Bear]]
        [entity.action() for entity in self.all_entities]
        [self.add_entity(new_entity) for new_entity in self.pending_entities]
        self.pending_entities.clear()
        for statistic in self.statistics['month'].keys():
             self.record.record_monthly_event(self.current_tick, "[{0}] {1}".format(self.statistics['month'][statistic], statistic))
        if self.current_tick % 12 == 0:
             self.annual_review()
        self.remove_dead_entities()
        self.current_tick += 1

    def annual_review(self):
        self.record.record_yearly_event(self.current_tick, 
                                        "Forest has {0} Trees, {1} Saplings, {2} Elder Trees, {3} Lumberjacks, and {4} Bears."\
                                        .format(len([tree for tree in self.population[Tree] if tree.alive and tree.tree_type == Tree.normal]),
                                                len([tree for tree in self.population[Tree] if tree.alive and tree.tree_type == Tree.sapling]),
                                                len([tree for tree in self.population[Tree] if tree.alive and tree.tree_type == Tree.elder_tree]),
                                                self.get_total_of_entity(Lumberjack),
                                                self.get_total_of_entity(Bear)))
        maw_accidents = self.statistics['year']['lumberjacks_mawed']
        if maw_accidents > 0:
            self.record.record_yearly_event(self.current_tick, "1 Bear captured by zoo.")
            self.kill_random_entity(Bear)
        else:
            self.record.record_yearly_event(self.current_tick, "1 new Bear added.")
            self.spawn_entities(Bear, [node for node in self.get_all_nodes() if not node.has(Bear)], 1)
        total_lumber_collected = self.statistics['year']['lumber_collected']
        # Shouldn't count dead lumberjacks, and we won't have removed them at this point
        # Dead lumberjacks harvest does count
        total_lumberjacks = self.get_total_of_entity(Lumberjack)
        if total_lumber_collected > total_lumberjacks:
            new_lumberjack_quantity = int(total_lumber_collected/10)
            self.spawn_entities(Lumberjack, 
                                [node for node in self.get_all_nodes() if not node.has(Lumberjack)],
                                new_lumberjack_quantity)
            self.record.record_yearly_event(self.current_tick, "{0} pieces of lumber harvested {1} new Lumberjack hired."\
                                                               .format(total_lumber_collected, 
                                                                       new_lumberjack_quantity))
        elif total_lumber_collected < total_lumberjacks:
            if total_lumberjacks > 1:
                self.kill_random_entity(Lumberjack)
                self.record.record_yearly_event(self.current_tick, "1 Lumberjack fired.")
        if (self.get_total_of_entity(Lumberjack) == 0):
            self.record.record_yearly_event(self.current_tick, "No Lumberjacks, 1 Lumberjack hired.")
            self.spawn_entities(Lumberjack, [node for node in self.get_all_nodes() if not node.has(Lumberjack)], 1)
        self.statistics['year'].clear()

    def remove_dead_entities(self):
        dead_entities = set([entity for entity in self.all_entities if not entity.alive])
        [entity.node.remove_entity(entity) for entity in dead_entities]
        for entity_type in self.population.keys():
            self.all_entities -= dead_entities
            self.population[entity_type] -= dead_entities

    def has_trees(self):
        return len(self.population[Tree]) > 0

    def __repr__(self):
        return '\n'.join([''.join([node.short() for node in row]) for row in self.layout])

class Looper(object):
    def __init__(self, forest):
        self.forest = forest

    def loop(self, screen):
        view = CursesView(forest, forest.statistics, forest.record)
        view.initialize()
    
        while forest.has_trees() and forest.current_tick <= args.duration:
            view.display(screen)
            forest.tick()
            sleep(args.sleep_time)

if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description='Simulate bears and lumberjacks wandering and interacting in a forest.')

    parser.add_argument('width', metavar='WIDTH', type=int, help='width of the forest')
    parser.add_argument('height', metavar='HEIGHT', nargs='?', type=int, help='height of the forest.  Defaults to width if not provided')
    parser.add_argument('-b', '--bears', action='store', default=0.02, dest='bears', type=float, help='Amount of forest to populate with bears.  Range 0-1.')
    parser.add_argument('-l', '--lumberjacks', action='store', default=0.1, dest='lumberjacks', type=float, help='Amount of forest to populate with lumberjacks. Range 0-1.')
    parser.add_argument('-t', '--trees', action='store', default=0.5, dest='trees', type=float, help='Amount of forest to populate with trees. Range 0-1.')
    parser.add_argument('-d', '--duration', action='store', default=4800, dest='duration', type=int, help='Number of months to simulate.')
    parser.add_argument('-p', '--pause', action='store', default=0.1, dest='sleep_time', type=float, help='Number of seconds to sleep between simulation steps.')

    args = parser.parse_args()

    if args.height == None:
        args.height = args.width

    forest = Forest(args.width, args.height, {Bear: args.bears, Lumberjack: args.lumberjacks, Tree: args.trees})
    forest.initialize()

    looper = Looper(forest)
 
    curses.wrapper(looper.loop)
