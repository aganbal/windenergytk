#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
## template.py
##
## Alec Koumjian (c) Thu Feb 25 10:22:29 2010
##
## Description goes here.
################################################################################
import numpy as np

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
    for freq in range(freq_start, freq_final, freq_step):
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
                
                vert_shear[i][n] = vert_shear[i][n-1] - freq**2 * sec_masses[n-1] * deflection[n-1] - f_cent[i][n] * slope[i][n-1]
                
                bend_moment[i][n] = (bend_moment[i][n-1] - vert_shear[i][n] * (sec_lengths[n-1] - f_cent[i][n] * (sec_lengths[n-1]**3/(3*e_i[n-1]))) + slope[i][n-1]*sec_lengths[n-1]*f_cent[i][n]) / (1 - f_cent[i][n] * sec_lengths[n-1]**2 / (2 * e_i[n-1]))
                
                slope[i][n] = slope[i][n-1] + bend_moment[i][n] * (sec_lengths[n-1]/e_i[n-1]) + vert_shear[i][n] * (sec_lengths[n-1]**2/ (2 * e_i[n-1]))
                
                deflection[i][n] = deflection[i][n-1] + slope[i][n-1] * sec_lengths[n-1] + bend_moment[i][n] * (sec_lengths[n-1]**2 / (2 * e_i[n-1])) + vert_shear[i][n] * (sec_lengths[n-1]**3 / (3 * e_i[n-1]))
        
        old_composite_deflection = composite_deflection
        composite_deflection = deflection[0][-1] - deflection[1][-1] * (slope[0][-1]/slope[1][-1])
        if np.sign(old_composite_deflection) != np.sign(composite_deflection):
            nat_frequencies.append(freq)
        
    return nat_frequencies
