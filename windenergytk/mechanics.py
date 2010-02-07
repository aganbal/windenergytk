#!/usr/bin/env python

################################################################################
# mechanics.py                                                                 #
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

def uniform_beam_vibrations(beam_length, area_moment_of_inertia, 
                            mass_per_length, modulus_of_elasticity, 
                            range, frequency_step):
    """Estimate the natural freq of uniform cantilevered beam (Euler)."""
    return 0

def nonuniform_beam_vibrations():
    """Estimate natural freq of nonuniform vibrating cantilevered beam (Myklestad)"""
    
    return 0

def hinge_spring_flapping(number_of_blades, rotor_radius, blade_chord, 
                          airfoil_lift_curve_slope, blade_pitch_angle, 
                          nonrotating_natural_freq, rotating_natural_freq, 
                          blade_mass, blade_offset, rotational_speed, 
                          tip_speed_ratio, wind_shear_coefficient, 
                          cross_flow, yaw_rate, air_density):
    """ """
    return 0

def rotational_natural_freq(number_of_nodes, list_of_inertias, 
                            list_shaft_stiffness, start_freq, 
                            ending_freq, freq_step):
    """Holzer method to find the natural frequency of a rotating system. """
    return 0

def rainflow_cycle_counting(tseries):
    """Perform a cycle counting analysis of timeseries using rainflow method."""
    return 0