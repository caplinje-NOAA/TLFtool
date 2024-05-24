# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 16:22:22 2023
Comprehensive module for fitting acoustic data
@author: james.caplinger
"""
# python imports
from dataclasses import dataclass

# general imports
import numpy as np
import scipy.stats as stats
import scipy.optimize as sciopt

# package level imports
from .utils.delta_method import delta_method



# Needs Reference for equation (though it is standard)

def dampedCylSpreading(r:np.ndarray,SL:float,alpha:float):
    """Caclulates transmission loss as a function of range, with damping/attenuation, where:
        SL = pseudo source level, 
        F = psuedo spreading coefficient,       
        alpha = attenuation (dB per units of r), 
        r = range.
        Signs of alpha and F are ignored"""

    return SL-10.0*np.log10(r)-np.abs(alpha)*r

def dampedGeoSpreading(r:np.ndarray,SL:float,F:float,alpha:float):
    """Caclulates transmission loss as a function of range, with damping/attenuation, where:
        SL = pseudo source level, 
        F = psuedo spreading coefficient,       
        alpha = attenuation (dB per units of r), 
        r = range.
        Signs of alpha and F are ignored"""

    return SL-np.abs(F)*np.log10(r)-np.abs(alpha)*r

# Needs Reference for equation (though it is standard)
def geoSpreading(r:np.ndarray,SL:float,F:float):
    """Caclulates transmission loss as a function of range, where:
        SL = pseudo source level, 
        F = psuedo spreading coefficient,       
        r = range.
        Sign of F is ignored"""

    return SL-np.abs(F)*np.log10(r)


# organized output for linear regression results
@dataclass
class linearOutput:
    ranges_fit: np.ndarray
    levels_fit: np.ndarray
    conf_upper: np.ndarray
    conf_lower: np.ndarray
    F: float
    SL: float
    Rsquared: float
    label: str
    
    def resultsText(self):
        results = f'Linear lsq fit:\n-----------------------\nF = {np.abs(self.F):.2f}\nSL = {self.SL:.2f} dB\nr value = {self.Rsquared:.4f}'
        print(results)
        return results
    
    def interpLevel(self,r:float):
        """Interpolate level at input range (m).
            Units of r must be meters"""
        return self.SL-np.abs(self.F)*np.log10(r)
    
    def interpRange(self,L:float):
        """""Interpolate range (m) at input level
            Output units are in meters."""
        return 10**((self.SL-L)/np.abs(self.F))
        
    
# organized output for damped spreading output
@dataclass
class dampedOutput:
    ranges_fit: np.ndarray
    levels_fit: np.ndarray
    conf_upper: np.ndarray
    conf_lower: np.ndarray
    F: float
    SL: float
    alpha: float
    Rsquared: float
    label: str
    
    def resultsText(self):
        results = f'Damped lsq fit:\n-----------------------\nF = {np.abs(self.F):.2f}\nSL = {self.SL:.2f} dB\nalpha = {self.alpha:.4f}dB/(units r)\nr value = {self.Rsquared:.4f}'
        print(results)
        return results
    
    def interpLevel(self,r:float):
        """Interpolate level at input range (m).
            Units of r must be meters"""
        return dampedGeoSpreading(r,self.SL, self.F, self.alpha)
    
    def interpRange(self,L:float):
        """""Interpolate range (m) at input level
            Output units are in meters."""
        def minfun(r):
            return np.abs(L-dampedGeoSpreading(r,self.SL, self.F, self.alpha))
        
        out = sciopt.minimize_scalar(minfun,bounds=[1,1e12],method='bounded')
        return out.x
        

def linTLfit(ranges_m:np.ndarray, levels_dB:np.ndarray,method='curvefit',confidenceInterval=0.05,newr_ext=0.1)->linearOutput:
    """Performs fits of acoustic data to the geometric spreading equation using either scipy's curvefit or scipy's stats.linregress.
    In the case curvefit is used, a confidence interval can be specified (e.g. 0.05 for 95%) to produce lower and upper confidence limits.
    Returns a dataclass containing a plottable range and level array, as well as the resulting TLcoef, SL, and Rsquared value. 
    SYNTAX
    fit = LinTLfit(ranges_m, levels_dB)
    INPUT
    - ranges_m = input data of locations of measurements in meters
    - levels_dB = input data of measured levels at each range
    - method = fitting method, 'curvefit' uses the scipy algorithm of the same name, 'linregress' uses scipy.stats.lineregress
    - confidenceInterval = confidence interval for bands (e.g. 0.05 for 95%), requires method='curvefit'
    - newr_ext = a fraction which specifies the amount to extend the output range axis beyond the measured points
    OUTPUT
    - result = linearOuput dataclass with fields:
        -ranges_fit: a higher resolution x-axis of ranges
        -levels_fit: the fit evaluated with optimal parameters along ranges_fit
        -conf_upper: the upper confidence interval evaluated at ranges_fit corresponding to confidenceInterval
        -conf_lower: the lower confidence interval evaluated at ranges_fit corresponding to confidenceInterval
        -F: the optimal spreading coefficient result
        -SL: the optimal source level (really just the y-intercept) result
        -Rsquared:  the resulting R squared
        -resultsText: a method that prints a summary of the results
        -interpLevel: a method for interpolating the fit at a particular range
        -interpRange: a method for interpolating the fit at a particular level   
    
    """
    
    # generate high resolution out range axis
    ranges_fit = np.logspace(np.log10(np.min(ranges_m)*(1-newr_ext)),np.log10(np.max(ranges_m)*(1+newr_ext)),num=1000)
    
    # fitting
    if method=='linregress':
        # perform linear regression
        regression = stats.linregress(np.log10(ranges_m),y=levels_dB, alternative='greater')
        SL = regression.intercept
        F = regression.slope
        Rsquared =regression.rvalue**2
        conf_upper, conf_lower = [None]*2
    
    if method=='curvefit':
        popt, pcov = sciopt.curve_fit(geoSpreading, ranges_m, levels_dB)
        SL = popt[0]
        F = popt[1]
        
        if confidenceInterval:
            deltaReturn = delta_method(pcov,popt,ranges_fit,geoSpreading,ranges_m,levels_dB,alpha=confidenceInterval)
            Rsquared = deltaReturn['rsquared']
            conf_upper = deltaReturn['upr_conf']
            conf_lower = deltaReturn['lwr_conf']
        else:
            Rsquared, conf_upper, conf_lower = [None]*3
            
    # evaluate fit for plotting    
    levels_fit = geoSpreading(ranges_fit, SL, F)
    
    return linearOutput(ranges_fit, levels_fit, conf_upper, conf_lower, F, SL, Rsquared, 'Geometric Spreading')


def dampedTLfit(ranges_m:np.ndarray, levels_dB:np.ndarray,DCS=False,confidenceInterval=0.05,newr_ext=0.1)->linearOutput:
    """Performs fits of acoustic data to damped geometric spreading equations using either scipy's curvefit.
    A confidence interval can be specified (e.g. 0.05 for 95%) to produce lower and upper confidence limits.
    Returns a dataclass containing a plottable range and level array, as well as the resulting TLcoef, SL, and Rsquared value. 
    SYNTAX
    fit = LinTLfit(ranges_m, levels_dB)
    INPUT
    - ranges_m = input data of locations of measurements in meters
    - levels_dB = input data of measured levels at each range
    - DCS = boolean indication if DCS should be assumed (e.g. F = 10.0)
    - confidenceInterval = confidence interval for bands (e.g. 0.05 for 95%), requires method='curvefit'
    - newr_ext = a fraction which specifies the amount to extend the output range axis beyond the measured points
    OUTPUT
    - result = linearOuput dataclass with fields:
        -ranges_fit: a higher resolution x-axis of ranges
        -levels_fit: the fit evaluated with optimal parameters along ranges_fit
        -conf_upper: the upper confidence interval evaluated at ranges_fit corresponding to confidenceInterval
        -conf_lower: the lower confidence interval evaluated at ranges_fit corresponding to confidenceInterval
        -F: the optimal spreading coefficient result
        -SL: the optimal source level (really just the y-intercept) result
        -alpha: damping (attenuation) coefficient in units of dB/(units r)
        -Rsquared:  the resulting R squared
        -resultsText: a method that prints a summary of the results
        -interpLevel: a method for interpolating the fit at a particular range
        -interpRange: a method for interpolating the fit at a particular level   
    
    """
    
    # generate high resolution out range axis
    ranges_fit = np.logspace(np.log10(np.min(ranges_m)*(1-newr_ext)),np.log10(np.max(ranges_m)*(1+newr_ext)),num=1000)
    
    if DCS:
        fitfun = dampedCylSpreading
        label = 'Damped Cylindrical Spreading'
    else:
        fitfun = dampedGeoSpreading
        label = 'Damped Geometric Spreading'
        
    popt, pcov = sciopt.curve_fit(fitfun, ranges_m, levels_dB)
    if confidenceInterval:
        deltaReturn = delta_method(pcov,popt,ranges_fit,fitfun,ranges_m,levels_dB,alpha=confidenceInterval)
        Rsquared = deltaReturn['rsquared']
        conf_upper = deltaReturn['upr_conf']
        conf_lower = deltaReturn['lwr_conf']
    else:
        Rsquared, conf_upper, conf_lower = [None]*3
        
    if DCS:
        SL = popt[0]
        F= 10.0
        alpha = popt[1]
    else:
        SL = popt[0]
        F = popt[1] 
        alpha = popt[2]        
            
    # evaluate fit for plotting    
    levels_fit = dampedGeoSpreading(ranges_fit, SL, F, alpha)
    
    return dampedOutput(ranges_fit, levels_fit, conf_upper, conf_lower, F, SL, alpha, Rsquared,label)






def testPlots():
    
    # an example showing a few different fits
    import matplotlib.pyplot as plt
    # generic data to fit (L dependent, r is independent)
    L = np.array([172.3,171.4,173,171.7,166.1,161.6,161.4,155.5])
    r = np.array([753,753,715,715,1999,4038,4038,8023])
    
    linfit = linTLfit(r, L,newr_ext=.999)
    linfit.resultsText()
    dfit = dampedTLfit(r,L,newr_ext=.99)
    dfit.resultsText()
    dcsfit = dampedTLfit(r,L,DCS=True,newr_ext=.95)
    dcsfit.resultsText()
    
    fig,(axl,axd,axdcs) = plt.subplots(3,1,sharex=True)
    
    axl.semilogx(r,L, linestyle = 'none', marker= 'o')
    axl.semilogx(linfit.ranges_fit,linfit.levels_fit)
    axl.fill_between(linfit.ranges_fit,linfit.conf_lower,linfit.conf_upper,alpha=0.25)
    axd.semilogx(r,L, linestyle = 'none', marker= 'o')
    axd.semilogx(dfit.ranges_fit,dfit.levels_fit)
    axd.fill_between(dfit.ranges_fit,dfit.conf_lower,dfit.conf_upper,alpha=0.25)
    axdcs.semilogx(r,L, linestyle = 'none', marker= 'o')
    axdcs.semilogx(dcsfit.ranges_fit,dcsfit.levels_fit)
    axdcs.fill_between(dcsfit.ranges_fit,dcsfit.conf_lower,dcsfit.conf_upper,alpha=0.25)
    
    
    



    
    
    