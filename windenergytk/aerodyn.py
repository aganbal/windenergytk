#!/usr/bin/env python

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
    return [0,0,0]

def linear_rotor_analysis(rct_matrix):
    """Uses a linear approx. of lift curve to estimate turbine rotor performance.
    
    INPUT
    rct_matrix: (numpy.ndarray) 3 x n array of fradius, chord, twist on each line
        fradius: fractional radius along blade
        chord: (float)
        twist: (float)
    OUTPUT
    linear_rotor_stats: (dict) with the following keys
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
    linear_rotor_stats = \
        {'total_radius': False,
        'tip_loss_factor': False,
        'angle_of_attack': False,
        'angle_of_rwind': False,
        'lift_coefficient': False,
        'drag_coefficient': False,
        'axial_induction_factor': False,
        'angular_induction_factor': False,
        'local_power_coefficient': False}
        
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
