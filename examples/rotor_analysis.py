#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# rotor_analysis.py                                                            #
#                                                                              #
# Part of UMass Amherst's Wind Energy Engineering Toolbox of Mini-Codes        #
#                   (or Mini-Codes for short)                                  #
#                                                                              #
# Python code by Alec Koumjian  -   akoumjian@gmail.com                        #
#                                                                              #
# This code demonstrates how to make use of the rotor analysis functions       #
# located in the aerodyn module.                                               #
#                                                                              #
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
from windenergytk.aerodyn import rotor_analysis


def demo_linear_analysis():
    """Demonstrates how to use the linear rotor analysis."""

    ## Set Input
    ## Radius, Chord, Twist matrix
    ## The rct matrix represents the actual blade design being analyzed.
    ## The designs are represented by dividing the blade into stations. Each
    ## station lists the fractional radius at the center of that staion,
    ## the chord length (which can be thought of as the cross sectional
    ## length) and twist.
    rct_matrix = [[.2, 2., .2],
                  [.4, 1.9, .4],
                  [.6, 1.9, .5],
                  [.8, 1.6, .7],
                  [1., 1.4, .9]]

    ## The second input of real interest are the lift curve and the drag
    ## curve. For a linear method, this will be tuples that include
    ## the slope and intercept of the line that will be used
    ## to approximate the curves.
    ## (slope, intercept)
    linear_lift_curve = (2., .3)
    linear_drag_curve = (.01, .1)

    ## The other inputs include a designed tip speed ratio
    ## the number of blades, the initial pitch relative to  the tip,
    ## the blade radius and the hub radius
    tsr = 10.
    number_blades = 3
    pitch_0 = .2
    hub_radius = .5
    blade_radius = 10.


    ## The returned values give characteristic information
    ## at each station provided in the original input.
    ## It returns the values as a n x 9 matrix (where n is the
    ## number of stations). A single station's values come
    ## as an array within the array
    ## [...,
    ## [local_radius, local_tip_loss, angle_of_attack,
    ##  angle_of_rwind, lift_coef, drag_coef,
    ##  axial_induc_factor, angular_induc_factor, local_power_coef],
    ##  ...]

    
    ## Note that we also specify either "linear" or "nonlinear" for the method.
    return rotor_analysis(rct_matrix, tsr, number_blades, pitch_0, blade_radius,
                          hub_radius, linear_lift_curve, linear_drag_curve,
                          "linear")

if __name__ == "__main__":
    results = demo_linear_analysis()
    print "Local properties for blade design"
    print "%16s %16s %16s %16s %16s" % ("radius","tip loss","angle of attack",
                                        "lift coefficient","power coefficient")
    for station in range(len(results)):
        print "%16.2f %16.2f %16.2f %16.2f %16.2f" % (results[station][0],
                                                      results[station][1],
                                                      results[station][2],
                                                      results[station][4],
                                                      results[station][-1])



