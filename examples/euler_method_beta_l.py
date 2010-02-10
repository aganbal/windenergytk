#!/usr/bin/env python
# -*- coding: utf-8 -*-


################################################################################
# euler_method_beta_l.py                                                                   #
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

import matplotlib.pyplot as plt
import numpy as np

# We want to find solutions to the equation:
# cosh(x)cos(x) + 1 = 0

# Plotting the solutions
# To get a better understanding of the solutions we're looking for, 
# we first rearrange the equation:
# cos(x) = -1/cosh(x)
# If we plot each side of the equation separately, the points where the two 
# functions intersect are solutions for the equation.
def show_graph():
    x = np.arange(-10, 10, 0.2)
    y = np.cos(x)
    y_2 = -1./np.cosh(x)
    fig = plt.figure()
    plt.grid()
    ax = fig.add_subplot(111)
    ax.plot(x, y,'-',x, y_2,'-')
    plt.axis([-10,10,-2,2])
    plt.show()

def epsilon(x):
    return np.cosh(x) * np.cos(x) + 1

def solve(number_of_solutions=3, y=0.0, step=1, target_epsilon=0.001):
    """Iteratively solve cosh(y)cos(y) + 1 = 0 for y using the Euler method"""
    
    solutions = []    
    while len(solutions) < number_of_solutions:
        y_1 = y
        y = y + step
        epsilon_y = epsilon(y)
        epsilon_y_1 = epsilon(y_1)
        if np.sign(epsilon_y) != np.sign(epsilon_y_1):
            while (abs(epsilon_y) > target_epsilon) and (abs(epsilon_y_1) > target_epsilon):
                n = (y_1 + y)/2
                epsilon_n = epsilon(n)
                epsilon_y = epsilon(y)
                epsilon_y_1 = epsilon(y_1)
                if np.sign(epsilon(n)) != np.sign(epsilon(y)):
                    y_1 = n
                else:
                    y = n
            if abs(epsilon_y) < abs(epsilon_y_1):
                solutions.append(y)
            else:
                solutions.append(y_1)
    return solutions




if __name__ == "__main__":
    print "The first three solutions for x are:"
    print solve()
    show_graph()

    