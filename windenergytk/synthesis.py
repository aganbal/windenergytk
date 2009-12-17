#!/usr/bin/env python

################################################################################
# synthesis.py                                                                 #
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

import numpy as np
import scikits.timeseries as ts

def find_bin(some_number, min, bins, value_range):
    """Find the bin (index) that a number falls into."""
    ## Zero out, multiply by ratio of bins to the range, add .5 for low values
    bin = round((some_number - min) * (bins/float(value_range)) + 0.5)
    if bin > bins:
        bin = bins
    if bin < 1:
        bin = 1
    
    ## Make integer data type
    bin = int(bin)
    ## Adjust for Python array starting index with 0
    bin -= 1
    return bin

def weighted_choice(cumu_prob_vector):
    """Returns random number (0 < x < 1) weighted by the probability vector."""
    return np.searchsorted(cumu_prob_vector, np.random.uniform())

def gen_arma(mean, stdev, autocor1, npoints):
    """Normally distributed timeseries using Autoregressive Moving Average."""
    ## Generate normally distributed noise array
    noise = np.random.normal(0, (1-autocor1**2)**.5, npoints)
    
    ## Create autoregressive list with noise
    ar_list = [0]
    for i in range(1, len(noise)):
        ar_list.append(autocor1 * ar_list[i-1] + noise[i])
    
    ## Adjust ARMA to have specified mean and stdev
    arma_array = []
    for index in range(len(ar_list)):
        arma_array.append(mean + stdev * ar_list[index])
    
    arma_ts = ts.time_series(data=arma_array, 
    start_date="01-01-2001",freq='T')
    
    return arma_ts


def gen_markov_tpm(tseries, bins):
    """Generate a Markov transition probability matrix from a timeseries."""
    ## Find range of values
    max = tseries.max()
    min = tseries.min()
    value_range = max - min
    
    ## Create empty NxN matrix
    tpm = np.zeros((bins, bins), dtype=np.float32)
    
    ## Tally number of transitions from one bin to another, save in matrix.
    for i in range(len(tseries)-1):
        ## Find bins
        source_bin = find_bin(tseries[i], min, bins, value_range)
        destination_bin = find_bin(tseries[i+1], min, bins, value_range)
        
        ## Add count to transition matrix
        ## Sources are rows, destinations are columns
        tpm[source_bin][destination_bin] += 1
    
    ## Total counts for each source bin
    totals = tpm.sum(axis=1)
    
    ## If a row of bins is empty, add one count for even probability
    for index in range(len(totals)):
        if totals[index] == 0:
            ## Makes every value in tpm[index] equal to 1
            tpm[index] = 1
            ## Don't forget to change the new sum
            totals[index] = bins
    
    ## Iterate over tpm and normalize values to probability
    for (row, column), value in np.ndenumerate(tpm):
        tpm[row][column] = float(value) / totals[row]
    
    return tpm
    
def gen_cumu_tpm(tpm):
    """Create cumulative transition probability matrix from regular tpm. """
    ## Turns tpm rows into cumulative rows
    cumu_tpm = np.cumsum(tpm, axis=1)
    
    return cumu_tpm
    
def gen_ts_from_tpm(tpm, bin_width, length, freq='T'):
    """
    Create timeseries using a Transisiton Probability Matrix
    INPUT: tpm  = ndarray of n*n values
           length (int)
    OUTPUT: tseries = timeseries of length
    """
    ## Create cumulative matrix from tpm
    cumu_tpm = gen_cumu_tpm(tpm)
    
    ## Initial wind range starts near median
    source_bin = int(len(cumu_tpm) / 2)

    ## Create empty array for wind speed data
    tseries_data = []

    ## Create wind speed data
    for index in range(length):
        ## Find wind range that random number falls into
        destination_bin = weighted_choice(cumu_tpm[source_bin])
        
        ## Create random wind speed within range of destination bin
        wind_speed = (destination_bin + np.random.uniform()) * bin_width
        
        ## Add wind speed to timeseries
        tseries_data.append(wind_speed)
        
        ## Destination bin becomes source bin
        source_bin = destination_bin
    
    ## Create timeseries out of tseries_data and freq
    tseries = ts.time_series(data=tseries_data, 
    start_date="01-01-2001",freq=freq)
    
    return tseries

def add_diurnal(tseries, sine_period, peak_mag):
    """
    Scales a time series to a sine wave of peak_mag with sine_period.
    Input: tseries, sine_period (float, hrs), peak_mag (float)
    Output: scaled_data (array-like)
    """
    # Convert sine_period to same frequency as tseries
    # Create a time delta of magnitude sine_period
    # Convert that time delta into frequency units same as tseries
    zero_date = ts.now('H')
    second_date = zero_date + sine_period
    time_delta = ts.date_array([zero_date, second_date])
    time_delta = time_delta.asfreq(tseries.freq)
    sine_period = float(time_delta[1] - time_delta[0])
    
    angular_freq = (2. * np.pi) / sine_period
    
    for i in range(len(tseries)-1):
        passed_time = float(tseries.dates[i]- tseries.start_date)
        sine_factor = peak_mag * np.sin(angular_freq * passed_time)
        tseries[i] = tseries[i] + tseries[i] * sine_factor
    
    return tseries

# Generate power density function (pdf) to create synthetic TPM from
# mean, stdev, autocorr, npointsx

def gen_pdf(desired_mean, desired_stdev, bin_width):
    return 0
## Essentially this is the reverse of the histogram