# -*- coding: utf-8 -*-
"""
File: estimate.py
Expert estimation tool for Monte Carlo simulation.

@author: Ron Rammage
"""

import unittest
import math
import random


class Estimate:
    ''' Class that abstracts estimates to provide trial cases for monte
    carlo simulation. Method "trial" provides random cases with 
    a triangular distribution."
        Defined by:
          best - best case estimate
          worst - worst case estimate
          likely - likely case estimate
          name - optional string describing the estimated event
    '''

    def __init__(self, best, worst, likely, title='unknown'):
        ''' Create a new estimate. '''
        if likely > worst:
            likely = worst
        if likely < best:
            likely = best

        self.best = best
        self.worst = worst
        self.likely = likely
        self.title = title
        
    def __triangular__(self, min_=0, max_=1, mode=0.5):
        """Return a random float in the range (min, max) inclusive
        with a triangular histogram, and the peak at mode.
        """
        u = random.random()
        if u <= (mode-min_)/(max_-min_):
            return min_ + math.sqrt(u*(max_-min_)*(mode-min_))
        else:
            return max_ - math.sqrt((1-u)*(max_-min_)*(max_-mode))
           
    def trial(self):
        ''' Returns an integer estimate that represents a simulated case based on estimate. '''
        return round(self.__triangular__(self.best, self.worst, self.likely))


class TestSuite(unittest.TestCase):
    ''' Suite of test cases for estimate class '''

    def test_construction(self):
        '''Creation of an estimate object shall contain best,
        worst, likely, and name parameters.'''
        best = 1
        worst = 100
        likely = 50
        name = 'TEST 1'
        test_estimate = Estimate(best, worst, likely, name)

        self.assertIsNotNone(test_estimate)

        self.assertEqual(test_estimate.best, best)
        self.assertEqual(test_estimate.worst, worst)
        self.assertEqual(test_estimate.likely, likely)
        self.assertEqual(test_estimate.title, name)

    def test_trail(self):
        '''Monte Carlo Simulation of symetric likely, best and worst
        shall generate an average value nearly equal to likely. '''
        total = 0
        best = 0
        worst = 100
        likely = 50
        number_of_trials = 1000
        test_estimate = Estimate(best, worst, likely)
        for i in range(1, number_of_trials):
            total += test_estimate.trial()

        mean = total / number_of_trials
        self.assertGreater(likely+2, mean)
        self.assertLess(likely-2, mean)

if __name__ == '__main__':
    unittest.main()
