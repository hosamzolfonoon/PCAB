# Getting familuar with dataset
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns

def pacb_histogram (filepath_input, filepath_output):
    # Read data frame
    pcab_query_response = pd.read_csv(filepath_input)

    # Definition color lists
    color_list = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']

    # Adjusting font size
    plt.rcParams.update({'font.size': 16})

    # number of Bins in Histogram
    k = 20

    # Histogram function
    def histogram_plot(ax, df, x, k, color_hist, histogram_title, x_label):#,xlable,ylable):
        '''x,y are lists and color_01 is name of color'''
        sns.histplot(df, x=x, bins=k, color=color_hist, ax=ax, kde=True)
        ax.set_title(histogram_title)
        #ax.set_xlim(0, 110)
        #ax.set_ylim(0, 0.3)
        #ax.grid(True)
        ax.set_xlabel(x_label)
        #ax.set_ylabel('Count')

    # Definigion of axes
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    fig, axs = plt.subplots(ncols=4, nrows=1, figsize=(30, 15))# constrained_layout=True)

    # Assignment of histogram parameters for 'Basic Time of Traffic histogram'
    color_hist = color_list[0]
    histogram_title = 'Basic Time of Traffic histogram' + '\n Bin: ' + str(k)
    ax = axs.flat[0]
    df = pcab_query_response
    x = pcab_query_response['basic_time_diff']
    x_label = 'Basic Time Difference'
    ## Drop 'NaN' from data
    x = x.dropna()
    ## Check for negative data, if there is, it means I have made a mistake
    neg = [x for x in x if x < 0]
    if len(neg) > 0:
        print('Error')
    histogram_plot(ax, df, x, k, color_hist, histogram_title, x_label)

    # Assignment of histogram parameters for 'Queries time histogram'
    color_hist = color_list[1]
    histogram_title = 'Queries time histogram' + '\n Bin: ' + str(k)
    ax = axs.flat[1]
    df = pcab_query_response
    x = pcab_query_response[pcab_query_response['Info_01'] == 'Query']['basic_time_diff']
    x_label = 'Queries Time'
    ## Drop 'NaN' from data
    x = x.dropna()
    ## Check for negative data, if there is, it means I have made a mistake
    neg = [x for x in x if x < 0]
    if len(neg) > 0:
        print('Error')
    histogram_plot(ax, df, x, k, color_hist, histogram_title, x_label)

    # Assignment of histogram parameters for 'Responces time histogram'
    color_hist = color_list[2]
    histogram_title = 'Responces time histogram' + '\n Bin: ' + str(k)
    ax = axs.flat[2]
    df = pcab_query_response
    x = pcab_query_response[pcab_query_response['Info_01'] == 'Response']['basic_time_diff']
    x_label = 'Responces Time'
    ## Drop 'NaN' from data
    x = x.dropna()
    ## Check for negative data, if there is, it means I have made a mistake
    neg = [x for x in x if x < 0]
    if len(neg) > 0:
        print('Error')
    histogram_plot(ax, df, x, k, color_hist, histogram_title, x_label)

    # Assignment of histogram parameters for 'Transmission time histogram'
    color_hist = color_list[3]
    histogram_title = 'Transmission time histogram' + '\n Bin: ' + str(k)
    ax = axs.flat[3]
    df = pcab_query_response
    x = pcab_query_response['Response_time_diff']
    x_label = 'Transmission Time'
    ## Drop 'NaN' from data
    x = x.dropna()
    ## Check for negative data, if there is, it means I have made a mistake
    neg = [x for x in x if x < 0]
    if len(neg) > 0:
        print('Error')
    histogram_plot(ax, df, x, k, color_hist, histogram_title, x_label)
    plt.savefig(filepath_output)

filepath_output_analysis = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Analysis Results'
filepath_output_histograms = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Pcab BoxPlot'

os.chdir(r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Analysis Results')
for file_01 in glob.glob('*.csv'):
    filepath_input_help = filepath_output_analysis + '\\' + file_01
    filepath_output_help = filepath_output_histograms + '\\' + file_01[:-4] + '_histogram.jpg'
    pacb_histogram(filepath_input_help, filepath_output_help)