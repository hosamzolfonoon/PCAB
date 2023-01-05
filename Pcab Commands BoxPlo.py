# Getting familuar with dataset
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns






filepath_output_analysis = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Analysis Results'
filepath_output_histograms = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Pcab Commands BoxPlots'

os.chdir(r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Analysis Results')
for file_01 in glob.glob('*.csv'):
    filepath_input_help = filepath_output_analysis + '\\' + file_01
    filepath_output_help = filepath_output_histograms + '\\' + file_01[:-4] + '_boxplot.jpg'
    pcab_boxplot(filepath_input_help, filepath_output_help)