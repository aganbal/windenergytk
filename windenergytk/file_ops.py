#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# file_ops.py                                                                  #
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

from scikits.timeseries import tsfromtxt as tsfromtxt
import numpy.ma


def sanitize(a_string):
    """
    Sanite string from leading/trailing whitespaces, make lowercase, etc.
    """
    ## Remove trailing spaces, make lowercase
    a_string = a_string.strip().lower()
    
    ## If string is just an integer, return it as such
    ## Otherwise just return the string
    try:
        final_string = int(a_string)
    except (ValueError, IndexError):
        final_string = a_string
    return final_string



def parse_file(dat_file):
    """Return meta and timeseries objects from WEC dat file.

    Input: opened WEC data file
    Output: Dictionary of timeseries with meta-data attached
    """
    
    meta = []
    trigger = False
    
    ## Append lines to meta until you reach the data.
    while not trigger:
        line = dat_file.readline().strip()
        meta.append(line)
        if '***' in line:
            dat_file.readline()
            dat_file.readline()
            trigger = True
    
    
    
    ## Create timeseries from dat_file
    ## Note: dat_file is at the correct seek() position from previous
    ## while loop
    timeseries = tsfromtxt(fname=dat_file,delimiter=',',datecols=0, freq='T'
    ,dtype=float)

    ## Separate timeseries
    ts_dict = separate_timeseries(timeseries)

    ## Create meta dictionary
    meta_dict = parse_meta(meta)
    
    ## Mask bad values
    for index in ts_dict.iterkeys():
        for value in meta_dict['filters'].itervalues():
            ts_dict[index] = numpy.ma.masked_values(ts_dict[index], value)
    

    
    ## Assign meta data to ts data
    meta_ts_dict = assign_meta(ts_dict, meta_dict)
    
    return meta_ts_dict
    
    
    

def parse_meta(meta_array):
    """
    Parse list of lines from .dat file into meaningful key/value pairs.
    Input: An array of lines from a WEC .dat file
    Output: Dictionary meta information
    """
    
    meta_dict = {'site_name':False,
    'location':False,
    'coords':{},
    'timezone':False,
    'elevation':False,
    'time_step':False,
    'logger_sampling':False,
    'time_period':False,
    'collector':False,
    'report_created':False,
    'sensors':{},
    'filters':{},
    'comments':False,
    }
    
    for line in meta_array:
        thistuple = line.partition(':') ## Split string into field/values
        
        ## Save field, values into separate variables
        line_key, line_values = thistuple[0],thistuple[2]
        
        ## Sanitize keys, values
        line_key, line_values = sanitize(line_key), sanitize(line_values)
        
        ## Name, location, time step, time period, comments, etc.
        if "site name" in line_key:
            meta_dict['site_name'] = line_values
        
        elif "location" in line_key:
            meta_dict['location'] = line_values
        
        elif "latitude" in line_key:
            lat = float(line_values)
            if "[s]" in line_key:
                lat *= -1
            meta_dict['coords']['latitude'] = lat
        
        elif "longitude" in line_key:
            lon = float(line_values)
            if "[w]" in line_key:
                lon *= -1
            meta_dict['coords']['longitude'] = lon
        
        elif "time zone" in line_key:
            meta_dict['timezone'] = line_values
        
        elif "elevation" in line_key:
            meta_dict['elevation'] = line_values
            
        elif "time step of data" in line_key:
            meta_dict['time_step'] = line_values
        
        elif "logger sample interval" in line_key:
            meta_dict['logger_sampling'] = line_values
        
        elif "report time period" in line_key:
            meta_dict['time_period'] = line_values
        
        elif "data collection by" in line_key:
            meta_dict['collector'] = line_values
    
        elif "report generated" in line_key:
            meta_dict['report_created'] = line_values
        
        elif "comments" in line_key:
            meta_dict['comments'] = line_values
        
        ## Categorize sensors
        elif "sensor #" in line_key:
            ## Sort out sensor information
            
            fields = ['name','type', 'designation', 'meters_above_ground'
            ,'units',]
            
            ## Extract number from first item: "Sensor #XX" returns XX
            sensor_number = int(line_key[int(line_key.find("#"))+1:])
            
            ## Create list of values
            values = line_values.split(",")
            
            ## Sanitize values
            for index in range(len(values)):
                values[index] = sanitize(values[index])
            
            ## Create dictionary for numbered sensor
            meta_dict['sensors'][sensor_number] = {}
            for index in range(0,len(values)):
                meta_dict['sensors'][sensor_number][fields[index]] = values[index]
        
        elif line_key[:2] == "-9":
            filter_value, filter_name = line_key.split(",")
            filter_value, filter_name = sanitize(filter_value)\
            ,sanitize(filter_name)
            meta_dict['filters'][filter_name] = int(filter_value)
        

    return meta_dict





def separate_timeseries(timeseries):
    """Take a multi column timeseries and separate into single timeseries."""
    ts_dict = {}
    for index in range(len(timeseries[0])):
        ts_dict[len(ts_dict)+1] = timeseries[:,index]
    return ts_dict
    
def assign_meta(ts_dict, meta_dict):
    """
    Assign meta information to recently separated timeseries.
    Input: ts_dict from separate_timeseries(), meta_dict from parse_meta()
    Output: Completed dictionary of timeseries with meta information
    """
    meta_ts_dict = {}
    ## Add timeseries
    for index, value in ts_dict.iteritems():
        meta_ts_dict[index] = {'timeseries': value}

    ## Add sensor specific meta info
    sensors = meta_dict.pop('sensors')

    for sensor_number, sensor_meta in sensors.iteritems():
        for index, value in sensor_meta.iteritems():
            meta_ts_dict[sensor_number][index] = value
    
    ## Add general meta info
    for key in meta_ts_dict.keys():
        for index, value in meta_dict.iteritems():
            meta_ts_dict[key][index] = value
    
    return meta_ts_dict
