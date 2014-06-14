import os, sys
sys.path.insert(0, os.path.abspath(".."))

from tree import Tree
import unittest

class ForestTestCase(unittest.TestCase):
    def test_increment_age_category(self):
        tree = Tree(None, 0, Tree.sapling)
        tree.increase_age(12)
        self.assertEqual(tree.tree_type, Tree.normal)

if __name__ == '__main__':
    unittest.main()
