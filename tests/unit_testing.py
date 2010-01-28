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
from windenergytk import synthesis
from windenergytk import aerodyn
from windenergytk import electrical
from windenergytk import dynamics
from windenergytk import performance

import scikits.timeseries as ts
import numpy



class AnalysisFunctions(unittest.TestCase):
    """Tests for the analysis module."""
    def setUp(self):
        """Create a scikites.timeseries object with set shape and size."""
        self.mu, self.sigma, self.size = 10, 2.5, 1000
        self.data = numpy.random.normal(self.mu, self.sigma, self.size)
        self.tseries = ts.time_series(self.data, start_date = "01-01-2001", freq="T")

    def test_dict_stat_values(self):
        """Test analysis.get_statistics() with dictionary output"""
        statistics_dict = analysis.get_statistics(self.tseries)
        self.assertEqual(type(statistics_dict), dict)
        self.assertAlmostEqual(statistics_dict['mean'], self.mu, 0)
        self.assertAlmostEqual(statistics_dict['std'], self.sigma, 0)
        self.assertEqual(statistics_dict['max'], self.data.max())
        self.assertEqual(statistics_dict['min'], self.data.min())
        self.assertEqual(statistics_dict['size'], self.data.size)
    
    def test_list_stat_values(self):
        """Test analysis.get_statistics() with list output"""
        statistics_list = analysis.get_statistics(self.tseries, output='list')
        self.assertEqual(type(statistics_list), list)
        self.assertAlmostEqual(statistics_list[0], self.mu, 0)
        self.assertAlmostEqual(statistics_list[1], self.sigma, 0)
        self.assertEqual(statistics_list[2], self.data.max())
        self.assertEqual(statistics_list[3], self.data.min())
        self.assertEqual(statistics_list[4], self.data.size)

    def test_histogram_data(self):
        """Test analysis.get_histogram_data()"""
        hdata = analysis.get_histogram_data(self.tseries, bins=10, normalized=True)
        numhdata = numpy.histogram(self.tseries, bins=10, normed=True)
        self.assertEqual(hdata[0].all(), numhdata[0].all())
        self.assertEqual(hdata[1].all(), numhdata[1].all())
    
    def test_weibull_params(self):
        """Testing analysis.get_weibull_params()"""
        ## Generate single variable weibull distribution
        c, k = 1., 1.5
        weibull_data = numpy.array(numpy.random.weibull(k, 10000))
        
        stats = analysis.get_statistics(weibull_data)
        
        ## generate params from distribution sample statistics
        test_c, test_k = analysis.get_weibull_params(stats['mean'],stats['std'])
        self.assertAlmostEqual(k, test_k, 1)
        self.assertAlmostEqual(c, test_c, 1)

class SynthesisFunctions(unittest.TestCase):
    """Tests for the synthesis functions."""
    def test_ARMA(self):
        """Testing synthesis.gen_arma()"""
        mean = 0.
        stdev = 1.
        autocor = .9
        size = 10000
        arma_ts = synthesis.gen_arma(mean, stdev, autocor, size)
        self.assertAlmostEqual(arma_ts.mean(), mean, 0)
        self.assertAlmostEqual(arma_ts.std(), stdev, 0)
        self.assertAlmostEqual(analysis.autocorrelate(arma_ts, 1)[1][1], autocor, 1)
        self.assertEqual(arma_ts.size, size)      
    
#    def test_gen_markov_tpm(self):
#        """Testing synthesis.gen_markov_tpm()"""
## TODO finish Synthesis Unit tests

class RotoraeroFunctions(unittest.TestCase):
    """Tests for the rotor aerodynamic functions."""
    def setUp(self):
        self.rct_matrix = [[0.1, 1.66, 31.3],
                           [0.2, 1.41, 18.3],
                           [0.3, 1.1, 11.6],
                           [0.4, 0.87, 7.7],
                           [0.5, 0.72, 5.2],
                           [0.6, 0.61, 3.5],
                           [0.7, 0.53, 2.3],
                           [0.8, 0.46, 1.3],
                           [0.9, 0.41, 0.6],
                           [1.0, 0.37, 0]]
        
        self.rotor_stats = \
        {'number_blades': 3,
        'total_radius': 10.,
        'hub_radius': 1.0,
        'tip_loss_factor': 0.0,
        'tip_speed_ratio': 7.0,
        'angle_of_attack': 7.0,
        'angle_of_rwind': 0.0,
        'lift_coefficient': 1.0,
        'drag_coefficient': 0.0,
        'axial_induction_factor': 0.0,
        'angular_induction_factor': 0.0,
        'local_power_coefficient': 0.0}
    
    def test_optimum_rotor(self):
        """Testing aerodyn.optimum_rotor()"""
        
        results = aerodyn.optimum_rotor(self.rotor_stats['lift_coefficient'],
                                        self.rotor_stats['angle_of_attack'], 
                                        self.rotor_stats['tip_speed_ratio'], 
                                        self.rotor_stats['total_radius'], 
                                        self.rotor_stats['hub_radius'], 
                                        self.rotor_stats['number_blades'], 
                                        len(self.rct_matrix))
        for i in range(len(results)):
            self.assertEqual(results[i], self.rct_matrix[i])
    
    def test_linear(self):
        """Testing aerodyn.linear_rotor_analysis()"""
        linear_stats = aerodyn.linear_rotor_analysis(self.rct_matrix)
        self.assertAlmostEqual(linear_stats['total_radius'], self.rotor_stats['total_radius'])
        self.assertAlmostEqual(linear_stats['tip_loss_factor'], self.rotor_stats['tip_loss_factor'])
        self.assertAlmostEqual(linear_stats['angle_of_attack'], self.rotor_stats['angle_of_attack'])
        self.assertAlmostEqual(linear_stats['angle_of_rwind'], self.rotor_stats['angle_of_rwind'])
        self.assertAlmostEqual(linear_stats['lift_coefficient'], self.rotor_stats['lift_coefficient'])
        self.assertAlmostEqual(linear_stats['drag_coefficient'], self.rotor_stats['drag_coefficient'])
        self.assertAlmostEqual(linear_stats['axial_induction_factor'], self.rotor_stats['axial_induction_factor'])
        self.assertAlmostEqual(linear_stats['angular_induction_factor'], self.rotor_stats['angular_induction_factor'])
        self.assertAlmostEqual(linear_stats['local_power_coefficient'], self.rotor_stats['local_power_coefficient'])
    
    def test_nonlinear(self):
        """Testing aerodyn.nonlinear_rotor_analysis()"""
        linear_stats = aerodyn.nonlinear_rotor_analysis(self.rct_matrix,
                                                        self.rotor_stats['angle_of_attack'],
                                                        self.rotor_stats['lift_coefficient'],
                                                        self.rotor_stats['drag_coefficient'])
        
        self.assertAlmostEqual(linear_stats['total_radius'], self.rotor_stats['total_radius'])
        self.assertAlmostEqual(linear_stats['tip_loss_factor'], self.rotor_stats['tip_loss_factor'])
        self.assertAlmostEqual(linear_stats['angle_of_attack'], self.rotor_stats['angle_of_attack'])
        self.assertAlmostEqual(linear_stats['angle_of_rwind'], self.rotor_stats['angle_of_rwind'])
        self.assertAlmostEqual(linear_stats['lift_coefficient'], self.rotor_stats['lift_coefficient'])
        self.assertAlmostEqual(linear_stats['drag_coefficient'], self.rotor_stats['drag_coefficient'])
        self.assertAlmostEqual(linear_stats['axial_induction_factor'], self.rotor_stats['axial_induction_factor'])
        self.assertAlmostEqual(linear_stats['angular_induction_factor'], self.rotor_stats['angular_induction_factor'])
        self.assertAlmostEqual(linear_stats['local_power_coefficient'], self.rotor_stats['local_power_coefficient'])


suite1 = unittest.TestLoader().loadTestsFromTestCase(AnalysisFunctions)
suite2 = unittest.TestLoader().loadTestsFromTestCase(SynthesisFunctions)
suite3 = unittest.TestLoader().loadTestsFromTestCase(RotoraeroFunctions)
alltests = unittest.TestSuite((suite1, suite2, suite3))
unittest.TextTestRunner(verbosity=2).run(alltests)