import fitsio as f
from matplotlib import pyplot as p
import numpy as np
import scipy.optimize as o

#get data from fits table
data = f.FITS('/Users/parkerhaggerty/Documents/allStar-l30e.2.fits')
cut = data[1].where('GLAT > -1 && GLAT < 1 && GLON > 80 && GLON < 100')
subset = data[1][cut]

#define a function to determine if outliers
def isOutlier(value, dataset):
    if((value < -999)):
        return True
    else:
        return False
        
#define functions to be fit
def line(t,a,b):
    return t*a +b
def quad(t,a,b,c):
    return a*(t**2) + b*t + c
    
#initial parameters    
param_guess_l = np.array([-1,1])    
param_guess_q = np.array([1,1,1])    
tdata = np.linspace(0.0,0.05,100)    
    
#create arrays for masked values
FE_H  = []
O_FE = []
lindata = []
quaddata = []

#mask bad values
for i in range(len(subset[:]['FE_H_ERR'])):
    if(isOutlier(subset[:]['FE_H_ERR'][i], subset[:]['FE_H_ERR'])==False):
        if(isOutlier(subset[:]['O_FE_ERR'][i], subset[:]['O_FE_ERR'])==False):
            FE_H.append(subset[:]['FE_H_ERR'][i])
            O_FE.append(subset[:]['O_FE_ERR'][i])
    
#optimize functions and make param arrays    
param_fit_l, pcov_l = o.curve_fit(line,FE_H,O_FE,p0=param_guess_l)
param_fit_q, pcov_q = o.curve_fit(quad,FE_H,O_FE,p0=param_guess_q)
print(param_fit_l, param_fit_q)

#get data for fit lines
for i in tdata:
    lindata.append(line(i, param_fit_l[0],param_fit_l[1]))
    quaddata.append(quad(i, param_fit_q[0],param_fit_q[1],param_fit_q[2]))

#graph
p.xlabel("FE_H_ERR")
p.ylabel("O_FE_ERR")
p.title("FE_H_ERR vs O_FE_ERR")
p.plot(FE_H,O_FE, '.')
p.plot(tdata, lindata, '#00b33c', linewidth=1, label='linear fit')
p.plot(tdata, quaddata, '#ff0000', linewidth=1, label='quadratic fit')
p.xlim(0, 0.05)
p.ylim(-0.2, 0.5)
p.legend()
p.show()