#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# aerodyn.py                                                                   #
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

from numpy import arctan, sin
from math import pi



## BEGIN HELPER FUNCTIONS

def q_terms(local_pitch, local_tsr, lift_coef_slope, lift_coef_intercept,
            local_solidity):
    """Create the q terms used in simplified angle of attack calculation.

    See Manwell, et. al Section 3.11 p. 138-39
    Please note that q1 and q3 are switched in Book vs. code
    INPUT
    local_pitch: (float)
    local_tsr: (floar)
    lift_coef_slope: (float)
    lift_coef_intercept: (float)
    local_solidity: (float)
    
    OUTPUT
    These terms are used in linear approximation of \alpha calculation
    q1: (float) 
    q2: (float)
    q3: (float)
    
    """
    d1 = numpy.cos(local_pitch) - local_tsr * numpy.sin(local_pitch)
    d2 = numpy.sin(local_pitch) + local_tsr * numpy.cos(local_pitch)
    
    q1 = (d1 * lift_coef_slope) + ((4 * local_tsr / local_solidity) *
                                          numpy.cos(local_pitch) * d2)
    
    q2 = d2 * lift_coef_slope + (d1 * lift_coef_intercept -
                                 (4 * local_tsr / local_solidity) *
                                 (d1 * numpy.cos(local_pitch) - d2 *
                                  numpy.sin(local_pitch)))
    
    q3 = d2 * lift_coef_intercept - ((4 * local_tsr / local_solidity) *
                                     d1 * numpy.sin(local_pitch))
    
    return q1, q2, q3


def calc_attack_angle(q1, q2, q3):
    """Calculate angle of attack for linear/small angle approximation.

    As seen in section 3.11 of Manwell, et. al.

    INPUT
    Q-terms as returned from q_terms().
    q1: (float)
    q2: (float)
    q3: (float)
    
    OUTPUT
    angle_of_attack: (float) local angle of attack in radians
    
    """
    return -(numpy.sqrt(q2 ** 2 - 4 * q1 * q3) - q2) / (2 * q1)


def calc_axial_factor(local_tip_loss, lift_coefficient, angle_of_rwind,
                      local_solidity):
    
    return 1 / (1 + (4 * local_tip_loss * (numpy.sin(angle_of_rwind) ** 2) /
                     (local_solidity * lift_coefficient *
                      numpy.cos(angle_of_rwind))))
    

def calc_angular_factor(axial_induc_factor, angle_of_rwind, local_tsr):
    
    return axial_induc_factor * numpy.tan(angle_of_rwind) / local_tsr

def tip_loss(number_of_blades, fractional_radius, angle_of_rwind):
    """This calculates the rotor tip loss using Prandtl method.
    
    Reference: deVries, Fluid Dynamics Aspects of Wind Energy Conversion.
    
    INPUT
    number_of_blades: (int)
    fractional_radius: (float) local radius / total radius
    angle_of_rwind: (float) angle of relative wind
    
    OUTPUT
    tip_loss: (float)
    """
    
    tmp = numpy.exp(-(number_of_blades / 2) * (1 - fractional_radius) / 
                     (fractional_radius * numpy.sin(angle_of_rwind)))
    
    if tmp > 0 and (1 - tmp**2) > 0:
        return numpy.arctan((numpy.sqrt(1 - tmp**2) / tmp) / (numpy.pi/2))
    else:
        return 1.
    
    return 0


def rotor_coefs(axial_induc_factor, angular_induc_factor, angle_of_rwind, 
                tip_speed_ratio, local_tsr, num_stations, local_solidity, 
                lift_coefficient, drag_coefficient, local_tip_loss):
    """Calculate local thrust, torque, and power coefficients.
    
    
    INPUT
    (all floating point numbers)
    
    OUTPUT
    local_thrust_coef: (float)
    local_torque_coef: (float)
    local_power_coef: (float
    """
    ## Note: uses formula 3.130 from Manwell, different than VB code
    local_thrust_coef = ((local_solidity * (1. - axial_induc_factor)**2 *  
                          (lift_coefficient * numpy.cos(angle_of_rwind) + 
                           drag_coefficient * numpy.sin(angle_of_rwind))) /
                         (numpy.sin(angle_of_rwind)**2))

    ## 3.134 from p. 137
    local_power_coef = ((8 /(tip_speed_ratio * num_stations)) * local_tip_loss * 
                        numpy.sin(angle_of_rwind)**2 * 
                        (numpy.cos(angle_of_rwind) - local_tsr *
                         numpy.sin(angle_of_rwind)) * 
                        (numpy.sin(angle_of_rwind) + local_tsr * 
                         numpy.cos(angle_of_rwind)) * 
                        (1 - (drag_coefficient / lift_coefficient) * 
                         (1/numpy.tan(angle_of_rwind))) * local_tsr**2)

    local_torque_coef = local_power_coef / local_tsr
    
    return local_thrust_coef, local_torque_coef, local_power_coef
## END HELPER FUNCTIONS



## BEGIN MAIN FUNCTIONS
def optimum_rotor(lift_coefficient, angle_of_attack, tip_speed_ratio,
                  total_radius, hub_radius, number_blades, sections):
    """Return blade station, chord, and twist for a given turbine.
    
    INPUT
    lift_coefficient: (float) airfoil lift coefficient at intended angle attack
    angle_of_attack: (float) angle of attack in degrees
    total_radius: (float) outer radius of turbine blades in meters
    hub_radius: (float) radius of hub, where blades begin
    number_blades: (int) number of turbine blades
    sections: (int) number of sections to divide blade length into
    
    OUTPUT
    rotor_design: (numpy.ndarray) 3 x sections array with station, chord, twist
        station: (float) distance from hub in meters
        chord: (float)
        twist: (float)
    
    """
    sct_matrix = []
    
    for r in range(sections):
        ## Calculate twist and chord for each section
        twist = arctan(2./(3.*tip_speed_ratio[r])) ## partial tip speed ratio ?
        chord = (8. * pi * r * sin(twist))/ (3. * number_blades *
                                             lift_coefficient *
                                             tip_speed_ratio[r])
        sct_matrix.append([r, twist, chord])
    return sct_matrix


def linear_rotor_analysis(rct_matrix, tip_speed_ratio, number_blades, pitch_0,
                          blade_radius, hub_radius, lift_coef_slope,
                          lift_coef_intercept, drag_coef_slope,
                          drag_coef_intercept):
    """Uses a linear approx. of lift curve to estimate turbine rotor performance.
    
    INPUT
    tip_speed_ratio: (float) The tip speed ratio
    number_blades:   (int) the number of blades
    pitch_0 :        (float) initial pitch angle relative to tip, deg
    blade_radius:          (float) radius in meters
    hub_radius:      (float) hub radius in meters
    lift_coef_slope: (float) slope of linear lift coefficient vs. AoA
    lift_coef_intercept: (float) intercept of linear coefficient vs. AoA line
    drag_coef_slope: (float) slope of 
    
    rct_matrix: (numpy.ndarray) 3 x n array of fradius, chord, twist on each line
        fradius: fractional radius along blade
        chord: (float)
        twist: (float)

    OUTPUT
    linear_rotor_stats: (ndarray) 6 x n, of the following
        angle_of_attack: (float) estimated angle of attack in degrees
        angle_of_rwind: (float) estimated angle of relative wind in degrees
        lift_coefficient: (float) linear approximation of lift coefficient
        drag_coefficient: (float) linear approximation of drag coefficient
        axial_induction_factor: (float)
        angular_induction_factor: (float)
        tip_loss_factor: (float) 

    power_coefficient: (float)
        
    """
    ## Convert all degrees to radians
    
    
    linear_rotor_stats = []
    total_power_coefficient = 0
    ## Loop over each station
    for j in range(len(rct_matrix)):
        ## local radius
        local_radius = rct_matrix[j][0] * blade_radius
        
        ## local chord
        local_chord = rct_matrix[j][1]
        
        ## local tip speed ratio
        local_tsr = tip_speed_ratio * rct_matrix[j][0]

        ## local solidity
        local_solidity = number_blades * local_chord / (2 * numpy.pi *
                                                       local_radius) 
        ## local pitch
        local_pitch = rct_matrix[j][2] + pitch_0
        
        local_tip_loss = 1
        tip_loss_epsilon = 1
        while tip_loss_epsilon > 0.01:

            ## Calculate q terms
            q1, q2, q3 = q_terms(local_pitch, local_tsr, lift_coef_slope,
                                 lift_coef_intercept, local_solidity)
        
            ## Calculate stats
            angle_of_attack = calc_attack_angle(q1, q2, q3)
            angle_of_rwind = local_pitch + angle_of_attack
            lift_coefficient = (angle_of_attack *
                                lift_coef_slope) + lift_coef_intercept
            axial_induc_factor = calc_axial_factor(local_tip_loss,
                                                   lift_coefficient,
                                                   angle_of_rwind,
                                                   local_solidity)

            angular_induc_factor = calc_angular_factor(axial_induc_factor,
                                                       angle_of_rwind,
                                                       local_tsr)
            drag_coefficient = (drag_coef_slope *
                                angle_of_attack) + drag_coef_intercept

            ## Calculate new tip loss
            old_local_tip_loss = local_tip_loss
            local_tip_loss = tip_loss(number_blades, rct_matrix[j][0], angle_of_rwind)
            tip_loss_epsilon = abs(local_tip_loss - old_local_tip_loss)
        
        ## Calculate local thrust, torque, and power coefficients 
        local_thrust, local_torque, local_power = \
            rotor_coefs(axial_induc_factor,angular_induc_factor, 
                        angle_of_rwind, tip_speed_ratio, local_tsr, 
                        len(rct_matrix), local_solidity, lift_coefficient, 
                        drag_coefficient, local_tip_loss)

        ## Add station's contribution to Power coefficient
        total_power_coefficient += local_power
            
        ## Add stats to results
        linear_rotor_stats.append([local_radius, local_tip_loss, 
                                   angle_of_attack, angle_of_rwind, 
                                   lift_coefficient, drag_coefficient, 
                                   axial_induc_factor, angular_induc_factor,
                                   local_power])

    ## Convert back to degrees
    
    return linear_rotor_stats



def nonlinear_rotor_analysis(rct_matrix, angle_of_attack, lift_coefficient, 
                             drag_coefficient):
    """Analyze wind turbine rotor using non-linear curves for lift and drag.
    
    INPUT
    rct_matrix: (numpy.ndarray) 3 x n array of fradius, chord, twist on each line
        fradius: fractional radius along blade
        chord: (float)
        twist: (float)
    angle_of_attack: (float) angle of attack
    lift_coefficient: (float) lift coefficient for rotor
    drag_coefficient: (float) drag coefficient for rotor
    
    OUTPUT
    nonlinear_rotor_stats: (dict) with the following keys
        total_radius: (float) optimal radius of rotor in meters
        tip_loss_factor: (float) 
        angle_of_attack: (float) estimated angle of attack in degrees
        angle_of_rwind: (float) estimated angle of relative wind in degrees
        lift_coefficient: (float) linear approximation of lift coefficient
        drag_coefficient: (float) linear approximation of drag coefficient
        axial_induction_factor: (float)
        angular_induction_factor: (float)
        local_power_coefficient: (float)
    
    """
    
    nonlinear_rotor_stats = \
        {'total_radius': False,
        'tip_loss_factor': False,
        'angle_of_attack': False,
        'angle_of_rwind': False,
        'lift_coefficient': False,
        'drag_coefficient': False,
        'axial_induction_factor': False,
        'angular_induction_factor': False,
        'local_power_coefficient': False}
        
    return nonlinear_rotor_stats
## END MAIN FUNCTIONS

if __name__ == "__main__":
    print "HI"
