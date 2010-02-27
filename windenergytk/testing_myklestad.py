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

def myklestad_beam_vibrations(sec_lengths, sec_masses, e_i, density, rpm, 
                              omega_start, omega_final, omega_step):
    """Estimate the natural freq of a nonuniform vibrating cantilevered beam.
    
    INPUT
    sec_lengths: (array-like) length of each section
    density: (float) density of material
    e_i: (array-like) structural stiffness, young's modulus * area inertia
    sec_mass: (array-like) mass of each section
    rpm: (float) rotations per minute
    omega_start: (float) starting low guess for natural frequency, rad/s
    omega_final: (float) high guess fo rnatural frequency, rad/s
    omega_step: (float) frequency step
    
    OUTPUT
    n_modes: (int) number of natural modes between omega_start and final
    omega: (array-like) list of natural frequencies
    """
    # MODS
    # No input for number of sections, redundant when there is a list
    # of lengths and masses
    # 
    # No need for Young's modulus if we are given structural stiffness (ei)
    # for each section
    
    return 0
