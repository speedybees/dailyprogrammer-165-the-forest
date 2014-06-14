import os, sys
sys.path.insert(0, os.path.abspath(".."))

from bear import Bear
from forest import Forest
from lumberjack import Lumberjack
from tree import Tree
import unittest

class ForestTestCase(unittest.TestCase):
    WIDTH = 2
    HEIGHT = 2

    def setUp(self):
        self.forest = Forest(ForestTestCase.WIDTH, ForestTestCase.HEIGHT, {Bear: 0.0, Lumberjack: 0.0, Tree: 0.0})
        self.forest.initialize()

    def tearDown(self):
        self.forest = None

    def test_spawn_entities(self):
        self.forest.spawn_entities(Bear, self.forest.get_all_nodes(), ForestTestCase.WIDTH * ForestTestCase.HEIGHT)
        for node in self.forest.get_all_nodes():
            self.assertEqual(len(node.entities), 1, 'not enough entities in node')

    def test_remove_entities(self):
        self.forest.spawn_entities(Bear, self.forest.get_all_nodes(), ForestTestCase.WIDTH * ForestTestCase.HEIGHT)
        for node in self.forest.get_all_nodes():
            self.forest.kill_random_entity(Bear)
        self.forest.remove_dead_entities()
        for node in self.forest.get_all_nodes():
            self.assertEqual(len(node.entities), 0, 'too many entities in node')

if __name__ == '__main__':
    unittest.main()
