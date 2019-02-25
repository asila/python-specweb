import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.covariance import EmpiricalCovariance, MinCovDet
from scipy import stats

# Absorbance data

spec =  pd.read_feather('/users/andrewsila/Downloads/OPUS_files/Raw_spectra.feather')

col = spec.columns.tolist()

meta = col[1:17]

spec.dtypes

[key for key in dict(spec.dtypes) if dict(spec.dtypes)[key] in ['float64']]

spectra = spec.select_dtypes(['float64'])

spectra = spectra.drop(['3996.481'], axis =  1)

spectra = spectra.drop(['499.8151'], axis =  1)

spectra.dtypes

wave = spectra.columns

# Plot spectra
fig=plt.figure(figsize=(8,6))
with plt.style.context(('ggplot')):
     plt.plot(wave,spectra.T)
     plt.xlabel('Wavenumbers (cm1)')
     plt.ylabel('Absorbance spectra')
     plt.show()

# Run PCA using sklearn
pca = PCA()

# Run PCA on scaled data and obtain the scores array
T = pca.fit_transform(StandardScaler().fit_transform(spectra))

# Scores plot of the first 2 PC
fig = plt.figure(figsize=(8,6))
with plt.style.context(('ggplot')):
    plt.scatter(T[:,0],T[:,1], edgecolors = 'k',cmap = 'jet')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('Score Plot')
plt.show()


# Next we define a metric to enable us detect an outlier
# Plot using the correct aspect ratio guided by the ylim and xlim ranges

fig = plt.figure(figsize=(8,6))
with plt.style.context(('ggplot')):
    plt.scatter(T[:,0],T[:,1], edgecolors = 'k',cmap = 'jet')
    plt.xlim(-180, 180)
    plt.ylim(-180, 180)
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('Score Plot')
plt.show()


# Compute the euclidean distance using the first 5 PC
euclidean = np.zeros(spectra.shape[0])
for i in range(10):
    euclidean += (T[:,i] - np.mean(T[:,:10]))**2/np.var(T[:,:10])


# Color code the scores plot using the euclidean distance  scale

colors = [plt.cm.jet(float(i)/max(euclidean)) for i in euclidean]
fig = plt.figure(figsize=(8,6))
with plt.style.context(('ggplot')):
    plt.scatter(T[:, 0], T[:, 1], c=colors, edgecolors='k', s=70)
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.xlim((-100, 100))
    plt.ylim((-100, 100))
    plt.title('Score Plot; Euclidean distance scale')
plt.show()

# A more unbiased method is to color code potential outliers using Mahalanobis distance

 
# fit a Minimum Covariance Determinant (MCD) robust estimator to data 
robust_cov = MinCovDet().fit(T[:,:10])
 
# Get the Mahalanobis distance
m = robust_cov.mahalanobis(T[:,:10])

# Color code the scores plot using Mahalanobis distance  scale

colors = [plt.cm.jet(float(i)/max(m)) for i in m]
fig = plt.figure(figsize=(8,6))
with plt.style.context(('ggplot')):
    plt.scatter(T[:, 0], T[:, 1], c=colors, edgecolors='k', s=70)
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.xlim((-100, 100))
    plt.ylim((-100, 100))
    plt.title('Score Plot: Mahalanobis scale')

# using seabon
sns.set_style('whitegrid')
sns.kdeplot(np.array(m), bw=0.5)
m = pd.Series(m)
m.describe()

#cut off
#ctl = 27 - (3*37)
ctu = 54 + (3*135)


[key for key in dict(spec.dtypes) if dict(spec.dtypes)[key] in ['object']]

meta = spec.select_dtypes(['object'])

m = pd.DataFrame(m)

m = m.join(meta)

hdw = meta.columns

hdw = list(hdw)

hdw.insert(0,"Maha")

m.columns = hdw

m[m.Maha > ctu]


m[m.Maha < ctu]




