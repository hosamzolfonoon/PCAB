'''
It is the main code to analyze pcab csv files and all actvities will applied as functions
'''
import os
import glob
from pcab_analysis import pcab_analysis
from pacb_histogram import pacb_histogram
from pcab_boxplot import pcab_boxplot


filepath_output_boxplots = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Pcab BoxPlots'
# Generating pcab analysis *csv 
os.chdir(r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Pcab Files')



