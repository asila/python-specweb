# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 10:49:46 2019

@author: LMumelo

edited on Mon Feb 05 2019
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go
import scipy.signal
from scipy.signal import find_peaks
from scipy.misc import electrocardiogram

# convert to a dataframe
os.chdir('/Users/andrewsila/Downloads/Babati')

spectra = pd.read_csv('afsis_iiss mir full range rounded off.csv')

# print the head of dataframe
print(spectra.head())

remH = spectra.rename(columns = lambda x : str(x)[1:])


mlt = pd.melt(remH, id_vars=['SN'])

x = mlt['variable']
y = mlt['value']

#Matplotlib Plots
plt.plot(x, y)
plt.show()

#Plotly Plots
data = [go.Scatter( x=mlt['variable'], y=mlt['value'],mode = 'lines' )]

pyo.plot(data, filename='pandas-time-series.html')

# Get individual SSNs

SN = list(set(list(mlt.SN)))

data = []

for sn in SN:
        sndf = mlt[mlt["SN"] == sn]
        trace = go.Scatter(
            x = sndf['variable'],
            y = sndf['value'],
            mode = 'lines',
            name = sn
        )
        colorscale='Jet',
        data.append(trace)
iplot(data, filename='line-mode')
    
'https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html'  

# Remove column with SSN
spect = spectra.drop(['SSN'], axis =  1)

wavenumbers = np.array(spect.columns)


# Make wavenumbers numeric
for i, str in enumerate(wavenumbers):
    wavenumbers[i] = str.replace('m','')
    
wavenumbers = list(map(float, wavenumbers))

wavenumbers = np.array(wavenumbers)


# Select ith row and make it an array
spec = np.array(spect.iloc[623])

#Matplotlib Plots
plt.subplot(2, 1, 1)
plt.plot(wavenumbers, spec)
#plt.show()

#find peak using different arguements
# 1. Prominence
peaks, _ = find_peaks(spec, prominence=0.1)

# 2. Distance
peaks2, _ = find_peaks(spec, distance = 1)

# 3. Width
peaks3, _ = find_peaks(spec, width = 20)

# 4. Threshold
peaks4, _ = find_peaks(spec, threshold = 0.2)

# Show for prominence only
plt.subplot(2, 1, 2)
plt.plot(wavenumbers[peaks], spec[peaks], "oc"); plt.plot(wavenumbers,spec); plt.legend(['prominence'])
plt.show()

# Loop to get all prominent peaks for each spctrum; and append their SSNs. Then melt to get a file of shape SSN and Peaks Wavenumbers

firstrow= spectra.iloc[[0]]
firstrow.plot(kind='line')
plt.show()

#Filter column range 2400:2300
Slicedf = spectra.loc[:,'m2401':'m2300.7']


#Get local maxima for each row
Slicedf['max_Value'] = Slicedf.max(axis=1)

#Get columns with Max values
Slicedf['Max_Columns'] = Slicedf.idxmax(axis=1)

#join SSN to sliceddf
SSn = pd.DataFrame(spectra['SSN'])
Joindf = SSn.join(Slicedf)

Joindf.to_csv('D:/maxVal_spectra.csv', index= False)
