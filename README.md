# python-specweb

This is a repo for specweb app developed for processing spectral data.

## Summary
The app is designed to include sub-components for performing specific functions:
* Reading binary files with spectral data.
* Quality control of individual sample spectrums and for assessing performance of instruments using internal standards.
* Calibration and prediction of diffrent soil, plant and fertilizer properties.

## Structure
Each sub-component will include a stand alone python script which are described below.

1. opus_reader: Reads and processes Bruker OPUS spectral files into data tables.
2. spec_qc: Finds peaks on a spectrum anc identifies presence/absence of carbonates then partitions a collection of spectra accordingly.
3. reference_selection
4. Calibration: Will provide a collection of machine learning methods for creating spectral calibrations models.
5. Prediction: Will provide an option of using global calibration models or user-driven models.


