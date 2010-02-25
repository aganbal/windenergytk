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

def myklestad_beam_vibrations(sec_lengths, young_mod, density, ei, n_sections, 
                              sec_mass, rpm, omega_start, omega_final, 
                              omega_step):
    """Estimate the natural freq of a nonuniform vibrating cantilevered beam.
    
    INPUT
    sec_lengths: (array-like) length of each section
    young_mod: (float) Young's modulus of material (modulus of elasticity)
    density: (float) density of material
    ei: (array-like) bending stiffness, modulus of elasticity * area moment of inertia
    n_sections: (int) number of sections
    sec_mass: (array-like) mass of each section
    rpm: (float) rotations per minute
    omega_start: (float) starting low guess for natural frequency, rad/s
    omega_final: (float) high guess fo rnatural frequency, rad/s
    omega_step: (float) frequency step
    
    OUTPUT
    n_modes: (int) number of natural modes between omega_start and final
    omega: (array-like) list of natural frequencies
    """
    i, j, slope, deflec, deflec1, omega1 = 0,0,0,0,0,0
    c_rotate1 = [0,0]
    c_rotate2 = [0,0]
    x_from_rotation_axis = np.zeros(n_sections)
    
    y_initial = [1, 0]
    theta_initial = [0, 1]
    
    # turn rpm into rad/s
    omega_rotate = rpm * np.pi / 60.
    
    slope_from_moment, slope_from_shear, \
    deflection_shear = influence(n_sections, sec_lengths, ei)
    
    x_from_rotation_axis[n_sections -1] = sec_lengths[0] / 2.
    
    for i in range(n_sections-2, 0, -1):
        x_from_rotation_axis[i] = x_from_rotation_axis[i+1] + sec_lengths[i]
    
    
        
    return 0
