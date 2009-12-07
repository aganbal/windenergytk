#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# unit_testing.py                                                              #
#                                                                              #
# Part of UMass Amherst's Wind Energy Engineering Toolbox of Mini-Codes        #
#                   (or Mini-Codes for short)                                  #
#                                                                              #
# Python code by Alec Koumjian  -   akoumjian@gmail.com                        #
#                                                                              #
# This code adapted from the original Visual Basic code at                     #
# http://www.ceere.org/rerl/projects/software/mini-code-overview.html          #
#                                                                              #
# These tools can be used in conjunction with the textbook                     #
# "Wind Energy Explained" by J.F. Manwell, J.G. McGowan and A.L. Rogers        #
# http://www.ceere.org/rerl/rerl_windenergytext.html                           #
#                                                                              #
################################################################################
#   Copyright 2009 Alec Koumjian                                               #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
################################################################################

import unittest
from windenergytk import analysis
import scikits.timeseries as ts
import numpy



class TestAnalysisFunctions(unittest.TestCase):
    """Tests for analysis.get_statistics() function."""
    def setUp(self):
        self.mu, self.sigma, self.size = 10, 2.5, 1000
        self.data = numpy.random.normal(self.mu, self.sigma, self.size)
        self.tseries = ts.time_series(self.data, start_date = "01-01-2001", freq="T")

    def testdictstatvalues(self):
        """Test get_statistics() with dictionary output"""
        statistics_dict = analysis.get_statistics(self.tseries)
        self.assertEqual(type(statistics_dict), dict)
        self.assertAlmostEqual(statistics_dict['mean'], self.mu, 0)
        self.assertAlmostEqual(statistics_dict['std'], self.sigma, 0)
        self.assertEqual(statistics_dict['max'], self.data.max())
        self.assertEqual(statistics_dict['min'], self.data.min())
        self.assertEqual(statistics_dict['size'], self.data.size)
    
    def testliststatvalues(self):
        """Test get_statistics() with list output"""
        statistics_list = analysis.get_statistics(self.tseries, output='list')
        self.assertEqual(type(statistics_list), list)
        self.assertAlmostEqual(statistics_list[0], self.mu, 0)
        self.assertAlmostEqual(statistics_list[1], self.sigma, 0)
        self.assertEqual(statistics_list[2], self.data.max())
        self.assertEqual(statistics_list[3], self.data.min())
        self.assertEqual(statistics_list[4], self.data.size)

    def testhistogramdata(self):
        """Test get_histogram_data()"""
        hdata = analysis.get_histogram_data(self.tseries, bins=10, normalized=True)
        numhdata = numpy.histogram(self.tseries, bins=10, normed=True)
        self.assertEqual(hdata[0].all(), numhdata[0].all())
        self.assertEqual(hdata[1].all(), numhdata[1].all())
    
    def testweibullparams(self):
        """Validate get_weibull_params()"""
        ## Generate single variable weibull distribution
        c, k = 1., 1.5
        weibull_data = numpy.array(numpy.random.weibull(k, 10000))
        
        stats = analysis.get_statistics(weibull_data)
        
        ## generate params from distribution sample statistics
        test_c, test_k = analysis.get_weibull_params(stats['mean'],stats['std'])
        self.assertAlmostEqual(k, test_k, 1)
        self.assertAlmostEqual(c, test_c, 1)
        


suite = unittest.TestLoader().loadTestsFromTestCase(TestAnalysisFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
