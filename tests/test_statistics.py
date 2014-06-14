import os, sys
sys.path.insert(0, os.path.abspath(".."))

from statistics import Statistics, StatisticsBatch
import unittest

class StatisticsBatchTestCase(unittest.TestCase):
    def setUp(self):
        self.statistics_batch = StatisticsBatch()

    def tearDown(self):
        self.statistics_batch = None

    def test_add_groups(self):
        self.statistics_batch.add_groups('month', 'year', 'all_time')
        self.assertEqual(len(self.statistics_batch.statistics), 3, 'not enough statistics in statistics batch')

    def test_log_all_groups(self):
        self.statistics_batch.add_groups('month', 'year', 'all_time')
        self.assertEqual(len(self.statistics_batch.statistics), 3, 'not enough statistics in statistics batch')
        self.statistics_batch.log_all('foo', 5)
        self.assertEqual(self.statistics_batch['month']['foo'], 5, '__getitem__ returned expected value')

if __name__ == '__main__':
    unittest.main()
