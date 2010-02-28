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
import numpy as np

def euler_beam_vibrations(beam_length, area_moment, mass_per_length, 
                          elastic_modulus, mode):
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
    frequency_constant = np.sqrt((elastic_modulus * area_moment) / mass_per_length) / (beam_length**2)
    
    
    # Use correct beta_l for mode
    if mode <= 4:
        beta_l = beta_l_list[mode-1]
    else:
        # beta_l approximates values of x for cos(x) = 0
        beta_l = mode*2.*np.pi - np.pi/2.
    
    # Calculate natural frequency for mode using Eqn. 4.2.31
    natural_freq = (beta_l**2) * frequency_constant
        
    # Calculate beta
    beta = beta_l / beam_length
            
    return natural_freq, beta


def myklestad_beam_vibrations(sec_lengths, sec_masses, e_i, density, 
                              rot_velocity, freq_start, freq_final, freq_step):
    """Estimate the natural freq of a nonuniform vibrating cantilevered beam.
    
    INPUT
    sec_lengths: (array-like) length of each section starting at free end
    sec_masses: (array-like) mass of each section
    e_i: (array-like) structural stiffness, young's modulus * area inertia
    density: (float) density of material
    rot_velocity: (float) rotational velocity in rad/s
    freq_start: (float) starting low guess for natural frequency, rad/s
    freq_final: (float) high guess fo rnatural frequency, rad/s
    freq_step: (float) frequency step
    
    OUTPUT
    nat_frequencies: (array-like) list of natural frequencies
    """
    # MODS
    # For explanation of how this works, see ../examples/explaining_myklestad.py
    # 
    # No input for number of sections, redundant when there is a list
    # of lengths and masses
    # 
    # No need for Young's modulus if we are given structural stiffness (ei)
    # for each section (not even used in VT function)
    # 
    # Clarify by using freq_* for oscillating frequency and rot_velocity
    # for rotational speeds
    #
    # Input rotational velocity as rad/s instead of rpm (use external function
    # to sanitize input)
    
    # 1. Setup prior to main algorithm
    
    # calculate number of stations
    n_stations = len(sec_lengths)
    
    # Create array of total distance from rotation axis for each mass
    dist_from_axis = np.empty(n_stations)
    dist_from_axis[0] = sec_lengths[0] / 2.
    for i in range(1, n_stations):
        dist_from_axis[i] = dist_from_axis[i-1] + \
        sec_lengths[i]
    
    # Create other empty arrays
    nat_frequencies = []
    slope = np.empty([2,n_stations])
    deflection = np.empty([2,n_stations])
    f_cent = np.empty([2,n_stations])
    vert_shear = np.empty([2,n_stations])
    bend_moment = np.empty([2,n_stations])
    
    # Initial conditions for two components
    initial_slope = [0, 1]
    initial_deflection = [1, 0]
    
    composite_deflection = 1
    
    # Iterate through range of possible natural frequencies
    for freq in np.arange(freq_start, freq_final, freq_step):
        # Calculate two sets of deflec/slope for linear combination
        for i in range(2):
            slope[i][0] = initial_slope[i]
            deflection[i][0] = initial_deflection[i]
            f_cent[i][0] = 0
            vert_shear[i][0] = 0
            bend_moment[i][0] = 0
            
            # Calculate forces/deflections at each station
            for n in range(1, n_stations):
                f_cent[i][n] = f_cent[i][n-1] + freq**2 * sec_masses[n-1] * dist_from_axis[n-1]
                
                vert_shear[i][n] = vert_shear[i][n-1] - freq**2 * sec_masses[n-1] * deflection[i][n-1] - f_cent[i][n] * slope[i][n-1]
                
                bend_moment[i][n] = (bend_moment[i][n-1] - vert_shear[i][n] * (sec_lengths[n-1] - f_cent[i][n] * (sec_lengths[n-1]**3/(3*e_i[n-1]))) + slope[i][n-1]*sec_lengths[n-1]*f_cent[i][n]) / (1 - f_cent[i][n] * sec_lengths[n-1]**2 / (2 * e_i[n-1]))
                
                slope[i][n] = slope[i][n-1] + bend_moment[i][n] * (sec_lengths[n-1]/e_i[n-1]) + vert_shear[i][n] * (sec_lengths[n-1]**2/ (2 * e_i[n-1]))
                
                deflection[i][n] = deflection[i][n-1] + slope[i][n-1] * sec_lengths[n-1] + bend_moment[i][n] * (sec_lengths[n-1]**2 / (2 * e_i[n-1])) + vert_shear[i][n] * (sec_lengths[n-1]**3 / (3 * e_i[n-1]))
        
        
        old_composite_deflection = composite_deflection
        composite_deflection = deflection[0][-1] - deflection[1][-1] * (slope[0][-1]/slope[1][-1])
        if (np.sign(old_composite_deflection) != np.sign(composite_deflection)) and (freq > freq_start):
            nat_frequencies.append(freq)
        
    return nat_frequencies


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
