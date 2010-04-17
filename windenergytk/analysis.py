#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# analysis.py                                                                  #
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

from numpy import histogram
from numpy import mean as npmean
import scikits.timeseries as ts
from scipy.special import gamma
from matplotlib.pyplot import psd


def get_statistics(timeseries, output='dictionary'):
    """
    Collects statistics from a timeseries object.
    
    Input: A timeseries object, output format ('dictionary' or 'list')
    Output: Dictionary or array of mean, stdev, max, min, size
    """
    stat_names = ['mean', 'std', 'max', 'min', 'size']
    stat_values = [timeseries.mean(), timeseries.std(),
    timeseries.max(), timeseries.min(),timeseries.size]
    
    if output == 'list':
        return stat_values
    else:
        tsdict = {}
        for index in range(5):
            tsdict[stat_names[index]] = stat_values[index]
        return tsdict

def get_histogram_data(timeseries, bins=10, normalized=True):
    """
    Returns histogram data of timeseries object
    Input: timeseries obj.
    Optional: No. of bins (default is 10), normalized (boolean)
    Output: Tuple (histogram, bin_edges)
    """
    return histogram(timeseries, bins, normed=normalized)

def get_weibull_params(mean, stdev):
    """
    Returns Weibull parameters c and k.
    Input: mean, stdev
    Output: Weibull scale: c, shape: k
    Citation: Manwell 2000, chapter 2"""
    if mean > 0:
        k = (stdev / mean)**-1.086
        c =  mean / gamma(1 + 1 / k)
    else:
        k, c = 0, 0
    return c, k


def crosscorrelate(timeseries1, timeseries2, max_lag_increment=False):
    """
    Returns crosscorrelation values at lag increments.
    Input: timeseries1, timeseries2
    Optional: max_lag_increment (int)
    Output: array of lags, array of correlation values
    """
    # If no max_lag_increment, do it for the length of timeseries
    if len(timeseries1) < len(timeseries2):
        smaller = timeseries1
    else:
        smaller = timeseries2
    if not max_lag_increment:
        max_lag_increment=len(smaller)
        
    # Create empty arrays, calculate means, std
    lag_values = []
    crosscorrelation_values = []
    difference_from_mean1, difference_from_mean2 = [],[]
    mean1,mean2 = timeseries1.mean(),timeseries2.mean()
    std1,std2 = timeseries1.std(),timeseries2.std()

    # Subtract mean from timeseries values, save as new arrays
    for array, timeseries, mean in [(difference_from_mean1, timeseries1, mean1),
                                    (difference_from_mean2,timeseries2, mean2)]:
        for value in timeseries:
            array.append(value-mean)

    # Do comparison at different lags
    for lag in range(0, max_lag_increment+1):
        mysum = 0
        for timestep in range(0,len(smaller)-lag):
            mysum += (difference_from_mean1[timestep] * \
            difference_from_mean2[timestep+lag])
            normalized_value = mysum / ((std1*std2)*(len(smaller)-lag))
        lag_values.append(lag)
        crosscorrelation_values.append(normalized_value)
    return lag_values, crosscorrelation_values

def autocorrelate(timeseries, max_lag_increment=False):
    """
    Returns autocorrelation values at lag increments.
    Input: a single timeseries object
    optional: max_lag_increment
    Output: Array of lags, Array of normalized autocorrelation values.
    """
    return crosscorrelate(timeseries, timeseries, max_lag_increment)

def block_average(timeseries, new_freq=''):
    """
    Reduce size of timeseries by taking averages of larger block size.
    Input: timeseries, new_freq (str) See scikits.timeseries doc
    Output: block averaged timeseries obj. in new frequency
    """
    # Label timeseries data with new frequency
    # ie: [5.5, 4.5] | [13-May-2009 11:40 13-May-2009 11:50] becomes
    #     [5.5, 4.5] | [13-May-2009 13-May-2009]
    timeseries = timeseries.asfreq(new_freq)

    # Create empty arrays, set first block_time
    current_block_values = []
    averages = []
    timesteps = []
    current_block_time = timeseries.dates[0]

    # For each index in timeseries, if the block of time has changed,
    # average the previous block values.  Otherwise keep adding
    # values to be averaged.
    for index in range(0,len(timeseries)):
        if current_block_time != timeseries.dates[index]:
            averages.append(npmean(current_block_values))
            timesteps.append(current_block_time)
            current_block_values = []
            current_block_time = timeseries.dates[index]
        current_block_values.append(timeseries[index])
    # Take average for last (or only) time block
    if current_block_values:
        averages.append(npmean(current_block_values))
        timesteps.append(current_block_time)
        

    # Return new block averages and timesteps as timeseries object
    return ts.time_series(averages,dates=timesteps)


def power_spectral_density(data_array, frequency, segment_size=256, window_method=False):
    """Return the power spectral density using matplotlib.pyplot.psd function."""
    return psd(data_array, NFFT=segment_size, Fs = frequency)


