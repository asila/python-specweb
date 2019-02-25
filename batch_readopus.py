import os
import opusFC
import numpy
import pandas
from ggplot import *
import csv

# Change current working directory to where OPUS files are stored in your computer
os.chdir('/users/andrewsila/studies/Charlotte/1716_points')

# Check currect working directory
cwd = os.getcwd()

file_list = os.listdir(cwd)

# Loop through files in file_list
L = []

#del file_list[0] # remove .DS_Store

file_list = glob.glob(cwd + "/*.[0-9]")

# .SNM
SNM = []
for f in file_list:
    dbs = opusFC.listContents(f)
    data = opusFC.getOpusData(f,dbs[0])
    SNM.append(data.parameters['SNM'])

# .INS
INS = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    INS.append(data.parameters['INS'])

# .DAT
DAT = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    DAT.append(data.parameters['DAT'])
    
# .TIM
TIM = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    TIM.append(data.parameters['TIM'])
    
# .DUR
DUR = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    DUR.append(data.parameters['DUR'])
    
# .CNM
CNM = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    CNM.append(data.parameters['CNM'])
    
# .RES
RES = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    RES.append(data.parameters['RES'])    

# .ZFF
ZFF = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    ZFF.append(data.parameters['ZFF'])

# .NPT
NPT = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    NPT.append(data.parameters['NPT'])
    
# .LWN
LWN = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    LWN.append(data.parameters['LWN'])

# .FXV
FXV = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    FXV.append(data.parameters['FXV'])

# .LXV
LXV = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    LXV.append(data.parameters['LXV'])

# .minY
minY = []
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    minY.append(data.minY)

# .maxY
maxY=[]
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    maxY.append(data.maxY)

# metadata
varnames = 'SNM','Instrument','Scan_date',"Time","Duration","Operator","Resolution","Zero_filling_Factor","Number_points","Laser_Wavenumber","Wavenumber_one","Wavenumber_last", "Min_absorbance", "Max_Absorbance"

metadata = numpy.vstack((SNM,INS,DAT,TIM,DUR,CNM,RES,ZFF,NPT, LWN, FXV, LXV,minY,maxY)).T

metadata = pd.DataFrame(metadata, columns= varnames)

print(metadata)

# Get absorbances and wavenumbers
wavenumbers = data.x

# Get Absorbance
# .maxY
absorb=[]
for f in file_list:
    data = opusFC.getOpusData(f,dbs[0])
    absorb.append(data.y)

spectra = pd.DataFrame(absorb, columns= wavenumbers)

# write metadata to a csv file
metadata.to_csv('OPUS files metadata.csv')

# write absorb to a csv file
spectra.to_csv('MIR spectra.csv') # Remember to add SSN

#ggplot(spec, aes(x="Wavenumbers", y="Absorbance")) + geom_line(color = "orange", size = 0.8) + scale_x_reverse() + ylim(0,data.maxY + (0.03 * data.maxY)) + ggtitle("Raw Spectrum") # Pad the maximum to avoid sitting at the border


