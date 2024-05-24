# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:46:49 2024

@author: jim
"""
 
from . import genericCSVhandler as gCSV


# levels to interpolate to, depending on metric
all_levels = {'SPL':[190,180,175,160,150,140],
              'SEL':[187,180,170,160,150,140],
              'Peak':[232,230,219,218,206,202]}

# short model names for column labels
shortModelNames = {'Geometric Spreading': 'GS', 'Damped Geometric Spreading':'DGS', 'Damped Cylindrical Spreading': 'DCS'}

# estimates ranges to each level, and prepares the data for a dash data_table
def getDistances(metric,fits):
    # get levels 
    levels = all_levels[metric]
    
    # build data columns
    columns = [{'id': 'Level (dB)', 'name': 'Level (dB)'}]
    for fit in fits:
        col = f'range (m), {shortModelNames[fit.label]}'
        
        columns = columns+[{'id': col, 'name': col}]
    # interpolate and build data    
    data = []
    for level in levels:
        row = {'Level (dB)':int(level)}
     
        for fit in fits:
            range_m = fit.interpRange(level)
            col = f'range (m), {shortModelNames[fit.label]}'
            
            row[col]=int(range_m)
            
        data.append(row)

    
    return data,columns

# files in data folder
filenames = {'OSW example 1': 'OSWex1.csv','OSW example 2': 'OSWex2.csv','OSW example 3': 'OSWex3.csv','User example':'user.csv'}

# loads example data, and prepares the data for a dash data_table
def getExData(dataset):
    
    rawData = gCSV.loadXYdata(f'data/{filenames[dataset]}')
    
    data = []
    for (r,l) in zip(rawData.x,rawData.y):
        row = {'range_m':r,'level':l}
        data.append(row)
        
    return data
        
    
    
