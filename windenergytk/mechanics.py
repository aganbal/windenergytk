#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import numpy

def euler_beam_vibrations(beam_length, area_moment, 
                            mass_per_length, elastic_modulus, mode):
    """Estimate the natural freq of uniform cantilevered beam.
    
    INPUT
    beam_length: (float) length of beam
    area_moment: (float) area moment of inertia for the beam
    mass_per_length: (float) the length density, mass per unit length
    elastic_modulus: (float) stress / strain
    mode: (int): The number mode to find a natural frequency for
    
    OUTPUT
    natural_frequency: (float) frequency for input mode
    beta: (float) parameter calculated from beta_l
    
    For reference see:
    Manwell Chapter 4 p. 153
    http://en.wikipedia.org/wiki/Euler–Bernoulli_beam_equation
    """
    # We are solving Eqn. 4.2.31 in Manwell et. al
    # natural_freq_i = (Beta*L)_i**2 * 1/L**2 * Sqrt((E I)/rho)
    
    # beta_l values are the solutions to the transcandental equation
    # cosh(beta_l)cos(beta_l) + 1 = 0
    # The first four solutions have been solved using the euler method
    # accurate to 11 digits of precision
    # For additional modes, solutions for beta_l approach cos(beta_l) +1 = 0
    # See ../examples/euler_method_demo.py
    
    beta_l_list = [1.8751040687129716, 4.6940911329743358, 
              7.8547574382376126, 10.995540734875467]
    
    # Now we calculate 1/L**2 * Sqrt((E I)/rho)
    frequency_constant = numpy.sqrt((elastic_modulus * area_moment) / mass_per_length) / (beam_length**2)
    
    
    # Use correct beta_l for mode
    if mode <= 4:
        beta_l = beta_l_list[mode-1]
    else:
        # beta_l approximates values of x for cos(x) = 0
        beta_l = mode*2.*numpy.pi - numpy.pi/2.
    
    # Calculate natural frequency for mode using Eqn. 4.2.31
    natural_freq = (beta_l**2) * frequency_constant
        
    # Calculate beta
    beta = beta_l / beam_length
            
    return natural_freq, beta

def myklestad_beam_vibrations(beam_length, area_moment_of_inertia,
                               mass_per_volume, modulus_of_elasticity, 
                               dimensions, angular_velocity,range, 
                               frequency_step):
    """Estimate the natural freq of a nonuniform vibrating cantilevered beam.
    'Inputs
    'aLength!() =length of section
    'eYoungs! = Young's modulus of material
    'rhoMaterial! = density of material
    'EI!() = stiffness of section
    'nSections% = number of sections
    'aMass!() = mass of section
    'rpm= rotational speed
    'omegaStart! = starting frequency in calculations, rad/s
    'omegaFinal! = ending frequency in calculations, rad/s
    'deltaOmega! = frequency step

beam_length,
area_moment_of_inertia,
mass_per_volume,
modulus_of_elasticity,
dimensions,
angular_velocity,
range, 
frequency_step,
"""
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
