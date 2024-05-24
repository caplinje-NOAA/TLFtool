# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 13:53:50 2023

@author: james.caplinger
Just a tiny generic csv loader
"""

import numpy as np

class dataContainer:
    x: np.ndarray=np.empty((1,))
    y: np.ndarray=np.empty((1,))
    n: int=0
     
    
def loadXYdata(path: str,sortData=True) -> dataContainer:
    def sort(data):
        sortedIndices = np.argsort(data.x)
        data.x = data.x[sortedIndices]
        data.y = data.y[sortedIndices]
        
    def update_n(data):
        if len(data.x)==len(data.y):
            data.n=len(data.x)
          
        else:
            Warning('x and y do not have the same length!')
   

    data = dataContainer()
    rawData = np.loadtxt(path,delimiter=',')
    data.x=rawData[:,0]
    data.y=rawData[:,1]
    update_n(data)
    if sortData:
        sort(data)
    return data
    
def removeDuplicateX(data:dataContainer,method='max')->dataContainer:
    """Removes duplicate x values if exist from digitized data, assuming data is sorted. y is taken to be max of values at duplicate x"""

    newx = []
    newy = []
    for x,y in zip(data.x,data.y):
        if not (x in newx): #detected duplicate
            newx.append(x)
            yatx = data.y[np.where(data.x==x)]
            # get lin vals
            if method=='dB mean':
                lin = 10**(yatx/10)
                newy.append(10*np.log10(np.mean(lin)))
           
            if method=='max':
                newy.append(np.max(yatx))
  
    out = dataContainer()
    out.x=np.array(newx)
    out.y=np.array(newy)
    out.n=len(out.x)
    
    return out
        
        