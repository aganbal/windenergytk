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

import numpy
from scipy.interpolate import interp1d


def deg_rad(conversion, *args):
    """Take an optional amount of values and convert between degrees/radians.

    INPUT
    conversion: (str) desired output, either 'degrees' or 'radians'
    *args: Will accept ints, floats, and ndarrrays (from NumPy)

    OUTPUT
    results: Original inputs converted to radians or degrees
    """
    ## set conversion factor
    if conversion == "radians":
        factor = (numpy.pi / 180.)
    else:
        factor = (180. / numpy.pi)
    
    results = []
    
    ## Iterate through each variable
    for arg in args:
        try:
            iterable = iter(arg)
        except TypeError:
            ## not iterable, just convert it
            arg = float(arg) * factor
            
        else:
            ## iterate over each index in possibly multi-d object
            for index in range(len(arg.flat)):
                arg.flat[index] = float(arg.flat[index]) * factor
                
        ## Add arg to results
        results.append(arg)

    return results


def q_terms(local_pitch, local_tip_loss, lift_coef_slope, lift_coef_intercept,
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
    These terms are used in linear approximation of alpha calculation
    q1: (float) 
    q2: (float)
    q3: (float)
    
    """
    d1 = numpy.cos(local_pitch) - local_tip_loss * numpy.sin(local_pitch)
    d2 = numpy.sin(local_pitch) + local_tip_loss * numpy.cos(local_pitch)
    
    q1 = (d1 * lift_coef_slope) + ((4 * local_tip_loss / local_solidity) *
                                          numpy.cos(local_pitch) * d2)
    
    q2 = d2 * lift_coef_slope + (d1 * lift_coef_intercept -
                                 (4 * local_tip_loss / local_solidity) *
                                 (d1 * numpy.cos(local_pitch) - d2 *
                                  numpy.sin(local_pitch)))
    
    q3 = d2 * lift_coef_intercept - ((4 * local_tip_loss / local_solidity) *
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

def linear_method_factors(fradius, number_blades, local_pitch, local_tsr,
                          lift_coef_slope, lift_coef_intercept, drag_coef_slope,
                          drag_coef_intercept, local_solidity):
    """Get angle of attack, relative wind, induction factors using linear curve.

    INPUT
    fradius:            (float) fractional radius of station
    number_blades:      (int) number of blades
    local_pitch:        (float) local pitch in radians
    local_tsr:          (float) local tip speed ratio
    lift_coef_slope:    (float) slope of linear lift coef vs. angle of attack
    lift_coef_intercept:(float) intercept of linear lift coef vs. AoA curve
    drag_coef_slope:    (float) same as lift 
    drag_coef_intercept:(float) same as lift
    local_solidity:     (float) local solidity
    
    OUTPUT
    local_tip_loss: (float)
    angle_of_attack: (float)
    angle_of_rwind: (float)
    lift_coefficient: (float)
    drag_coefficient: (float)
    axial_induc_factor: (float)
    angular_induc_factor: (float
    """
    local_tip_loss = 1
    tip_loss_epsilon = 1
    while tip_loss_epsilon > 0.01:
        
        ## Calculate q terms
        q1, q2, q3 = q_terms(local_pitch, local_tip_loss, lift_coef_slope,
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
        local_tip_loss = tip_loss(number_blades, fradius, angle_of_rwind)
        tip_loss_epsilon = abs(local_tip_loss - old_local_tip_loss)

        
        
    return local_tip_loss, angle_of_attack, angle_of_rwind, lift_coefficient,\
           drag_coefficient, axial_induc_factor, angular_induc_factor

def nonlinear_method_factors(fradius, number_blades, local_pitch, local_tsr,
                             lift_curve, drag_curve, local_solidity):
    """Get angle of attack, relative wind, induction factors w/ nonlinear curve.

    INPUT
    fradius:            (float) fractional radius of station
    number_blades:      (int) number of blades
    local_pitch:        (float) local pitch in radians
    local_tsr:          (float) local tip speed ratio
    lift_curve:         (float) array of empirical lift_coef vs. AoA curve
    drag_curve:         (float) array of empirical drag_coef vs. AoA curve
    local_solidity:     (float) local solidity
    
    OUTPUT
    local_tip_loss: (float)
    angle_of_attack: (float)
    angle_of_rwind: (float)
    lift_coefficient: (float)
    drag_coefficient: (float)
    axial_induc_factor: (float)
    angular_induc_factor: (float)
    """
    ## TODO
    ## Remove all but necessary calculations from loop

    lift_coef_epsilon = 10.
    angle_of_attack = 0.
    
    ## increment of "1 deg" in radians for changing AoA
    angle_delta = 0.0174532925

    ## Transpose curves to make interpolation easier
    ## Going from [[AoA, lift_coef]..] to
    ## [[AoA, AoA2...],[lift_coef, lift_coef2]]
    lift_curve = numpy.array(lift_curve).transpose()
    drag_curve = numpy.array(drag_curve).transpose()
    
    ## Find where empirical and Blade Element Momentum Theory
    ## lift coef vs. angle of attack curves meet
    while (lift_coef_epsilon > 0.01) and (angle_delta > 0.001):
        
        angle_of_rwind = local_pitch + angle_of_attack
        local_tip_loss = tip_loss(number_blades, fradius, angle_of_rwind)

        ## Use input lift coef vs. angle of attack
        interp_lift_curve = interp1d(lift_curve[0],lift_curve[1])
        empirical_lift_coef = float(interp_lift_curve(angle_of_attack))
        
        ## From 3.10.1.3 Manwell et. al.
        bemt_lift_coef = ((local_tip_loss / local_solidity) * 4 *
                          numpy.sin(angle_of_rwind) *
                          ((numpy.cos(angle_of_rwind) -
                            local_tsr * numpy.sin(angle_of_rwind)) /
                           (numpy.sin(angle_of_rwind) + local_tsr *
                            numpy.cos(angle_of_rwind))))

        ## Calculate axial induction factor
        axial_induc_factor = calc_axial_factor(local_tip_loss,
                                                   empirical_lift_coef,
                                                   angle_of_rwind,
                                                   local_solidity)
        ## Calculate angular induction factor
        angular_induc_factor = calc_angular_factor(axial_induc_factor,
                                                      angle_of_rwind, local_tsr)

        ## Calculate difference between points on two lines
        old_lift_coef_epsilon = lift_coef_epsilon
        lift_coef_epsilon = abs(empirical_lift_coef - bemt_lift_coef)

        ## if solution is approaching, keep incrementing AoA
        if lift_coef_epsilon < old_lift_coef_epsilon:
            angle_of_attack += angle_delta
        ## otherwise we've gone too far. Go back and make increment smaller
        else:
            angle_of_attack -= angle_delta
            angle_delta = .707 * angle_delta
            angle_of_attack += angle_delta

            
    interp_drag_curve = interp1d(drag_curve[0],drag_curve[1])
    drag_coefficient = float(interp_drag_curve(angle_of_attack))

    return local_tip_loss, angle_of_attack, angle_of_rwind, empirical_lift_coef,\
           drag_coefficient, axial_induc_factor, angular_induc_factor

        
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
    rotor_design: (numpy.ndarray) sections x 3 array with station, chord, twist
        station: (float) fractional distance of blade section
        chord: (float)
        twist: (float)
    
    """
    sct_matrix = []
    
    for r in range(sections):
        ## Calculate twist and chord for each section
        twist = numpy.arctan(2./(3.*tip_speed_ratio[r])) 
        chord = (8. * numpy.pi * r * numpy.sin(twist))/ (3. * number_blades *
                                             lift_coefficient *
                                             tip_speed_ratio[r])
        sct_matrix.append([r, twist, chord])
    return sct_matrix


def rotor_analysis(rct_matrix, tip_speed_ratio, number_blades, pitch_0,
                   blade_radius, hub_radius, lift_curve, drag_curve, method):
    """Returns performance statistics of a rotor.
    
    INPUT
    tip_speed_ratio: (float) The tip speed ratio
    number_blades:   (int) the number of blades
    pitch_0 :        (float) initial pitch angle relative to tip, deg
    blade_radius:          (float) radius in meters
    hub_radius:      (float) hub radius in meters
    lift_curve:       (array-like) either linear slope and intercept or
                                  emperical C_l vs. AoA points
    drag_curve:       (array-like) either linear slope and intercept or
                                  emperical C_d vs. C_l points
    

    
    rct_matrix: (numpy.ndarray) 3 x n array of fradius, chord, twist on each line
        fradius: (float) nondimensional fractional radius along blade
        chord:   (float) nondimensional length
        twist:   (float) in degrees

    OUTPUT
    rotor_stats: (ndarray) 7 x n, of the following
        angle_of_attack: (float) estimated angle of attack in degrees
        angle_of_rwind: (float) estimated angle of relative wind in degrees
        lift_coef: (float) linear approximation of lift coefficient
        drag_coef: (float) linear approximation of drag coefficient
        axial_induc_factor: (float)
        angular_induc_factor: (float)
        tip_loss_factor: (float)
        local_power_coef: (float) local power coefficient

    """
    ## Convert all degrees to radians
    pitch_0, rct_matrix[:,2] = deg_rad("degrees", pitch_0, rct_matrix[:,2])


    
    rotor_stats = []
    ## Loop over each station
    for j in range(len(rct_matrix)):
        ## Calculate method-independent station characteristics
        local_radius = rct_matrix[j][0] * blade_radius
        
        local_chord = rct_matrix[j][1]
        
        local_tsr = tip_speed_ratio * rct_matrix[j][0]

        local_solidity = number_blades * local_chord / (2 * numpy.pi *
                                                       local_radius) 
        local_pitch = rct_matrix[j][2] + pitch_0

        ## Calculate method dependent characteristics
        if method == "linear":
            (local_tip_loss, angle_of_attack, angle_of_rwind, lift_coef,
            drag_coef, axial_induc_factor, angular_induc_factor) =\
                       linear_method_factors(rct_matrix[j][0], number_blades,
                                             local_pitch, local_tsr,
                                             lift_curve[0], lift_curve[1],
                                             drag_curve[0], drag_curve[1],
                                             local_solidity)
        else:
            (local_tip_loss, angle_of_attack, angle_of_rwind, lift_coef,
            drag_coef, axial_induc_factor, angular_induc_factor) = \
                       nonlinear_method_factors(rct_matrix[j][0], number_blades,
                                                local_pitch, local_tsr,
                                                lift_curve, drag_curve,
                                                local_solidity)
            
                
        ## Calculate local thrust, torque, and power coefficients
        ## from method dependent results
        local_thrust, local_torque, local_power_coef = \
            rotor_coefs(axial_induc_factor,angular_induc_factor, 
                        angle_of_rwind, tip_speed_ratio, local_tsr, 
                        len(rct_matrix), local_solidity, lift_coef, 
                        drag_coef, local_tip_loss)


            
        ## Add stats to results
        rotor_stats.append([local_radius, local_tip_loss, 
                                   angle_of_attack, angle_of_rwind, 
                                   lift_coef, drag_coef, 
                                   axial_induc_factor, angular_induc_factor,
                                   local_power_coef])

    ## Convert back to degrees
    
    return rotor_stats


## For Testing
## rotor_analysis([[.2,2.,.3],[.4,2.,.4],[.6,2.,.5],[.8,2.,.6],[.9,2,.6],[.9,2.,.6]], 10., 3, .1, 10., 1., [[0.,0.],[1.,30],[1.5,40]],[[0.,0.],[1.,30],[1.5,40]], "nonlinear")
