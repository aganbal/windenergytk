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

def influence(n_sections, sec_lengths, ei):
    """Used to obtain the influence coefficients from the length and stiffness of each section
    
    INPUT
    n_sections: (int) number of sections
    sec_lengths: (array-like) length of each section
    ei: (array-like) stiffness of each section
    
    OUTPUT
    slope_from_moment: (array-like) 
    slope_from_shear: (array-like) slope at each point caused by shear force
    deflection_shear: (array-like) deflection at each section caused by shear
    
    """
    slope_from_moment = []
    slope_from_shear = []
    deflection_shear = []
    
    for i in range(n_sections):
        slope_from_moment[i] = sec_lengths[i] / ei[i]
        slope_from_shear[i] = slope_from_moment[i] * sec_lengths[i] / 2.
        deflection_shear[i] = slope_from_shear[i] * sec_lengths[i] * 2. / 3.
    
    return slope_from_moment, slope_from_shear, deflection_shear

def myklestad_beam_vibrations(sec_lengths, sec_masses, e_i, density, 
                              rot_velocity, freq_start, freq_final, freq_step):
    """Estimate the natural freq of a nonuniform vibrating cantilevered beam.
    
    INPUT
    sec_lengths: (array-like) length of each section
    sec_mass: (array-like) mass of each section
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
    
    # Create empty arrays
    slope = np.empty([2,len(sec_lengths)])
    deflection = np.empty([2,len(sec_lengths)])
    f_cent = np.empty([2,len(sec_lengths)])
    vert_shear = np.empty([2,len(sec_lengths)])
    bend_moment = np.empty([2,len(sec_lengths)])
    
    # Initial conditions for two components
    initial_slope = [0, 1]
    initial_deflection = [1, 0]
    
    
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
            for n in range(len(sec_lengths)):
                
    
    return 0
