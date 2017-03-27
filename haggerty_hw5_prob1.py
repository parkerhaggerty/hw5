# Import stuff...
import numpy as np
from scipy.optimize import curve_fit
import pylab as plt
from math import pi 


# Read in Data file ("munich_temperatures_average_with_bad_data.txt")...
data = np.loadtxt("munich_temperatures_average_with_bad_data.txt", dtype=float)
time=[]         # modified time data
temp=[]         # modified temperature data
tdata=np.linspace(2008, 2012, 10000)

rr= data[:,0]   # time (unmodified)
ss= data[:,1]   # temp (unmodified)

initial_fit_array=[]    # creates array for plotting purposes
data_fit_array=[]       # creates array for plotting purposes


# Creates new arrays for both time and temp (2008-2012) and masks bad values...
for i in range(len(rr)):
    if (2008 <= rr[i] <= 2012):
        if ((np.mean(ss) - 2*np.std(ss)) < ss[i] < (np.mean(ss) + 2*np.std(ss))):
            time.append(rr[i])
            temp.append(ss[i])


# Guesses
guess_freq = 1.0
guess_amplitude = 20.0
guess_phase = 0.0
guess_offset = np.mean(temp)
guess_parameters = [guess_amplitude, guess_phase, guess_offset]


# Create the function we want to fit
def my_function(t, a, b, c):
    return a*np.cos(2*pi*t+b)+c


# Do the fit
fit,pcov = curve_fit(my_function, time, temp, p0=guess_parameters)



for j in tdata:
    data_fit_array.append(my_function(j, fit[0], fit[1], fit[2]))

#print(fit[0], fit[1], fit[2])



# Populate arrays for plotting purposes
#for j in range(len(time)):
    #data_first_guess = my_function(time[j], *guess_parameters)
    #initial_fit_array.append(data_first_guess)


#for k in range(len(time)):
    #data_fit = my_function(time[k], fit[0], fit[1], fit[2])
   # data_fit_array.append(data_fit)


#print(fit)
#print(initial_fit_array)
#print('\n')
#print(data_fit_array)

# We'll use this to plot our first estimate
#data_first_guess = my_function(time, *p0)

# Recreate fitted curve using optimized parameters
#data_fit = my_function(time, *fit[0])


plt.title("Temperature In Munich")
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.xlim(2008, 2012)
plt.ylim(-15, 30)
plt.plot(time, temp, label='data')
plt.plot(tdata, data_fit_array, '#ff0000', linewidth=2, label='fit')
plt.legend()
plt.show()