# Getting familuar with dataset
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def pcab_boxplot (filepath_input, filepath_output):
    print(filepath_input)
    # Read data frame
    pcab_query_response = pd.read_csv(filepath_input)

    # Definition color lists
    color_list = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']

    # Adjusting font size
    plt.rcParams.update({'font.size': 14})

    # Box Plotn function
    def box_plot(ax, x, color_box, x_label, number_samples):
        '''x,y are lists and color_01 is name of color'''
        pcab_query_response = pd.read_csv(filepath_input)
        # finding the 1st quartile
        q1 = np.quantile(x, 0.25).round(8)
        # finding the 3rd quartile
        q3 = np.quantile(x, 0.75).round(8)
        med = np.median(x).round(8)
        mean = np.mean(x).round(8)
        # finding the iqr region
        iqr = q3-q1
        # finding upper and lower whiskers
        upper_bound = (q3+(1.5*iqr)).round(8)
        lower_bound = (q1-(1.5*iqr)).round(8)
        outlyer_up = (x > upper_bound).sum()
        outlyer_down = (x < lower_bound).sum()
        lower_bound = ("{:f}".format(lower_bound))
        boxplot_title = ('\n iqr: ' + str(iqr) +
        '\n Upper Bound: ' + str(upper_bound) +
        '\n Lower_Bound: ' + str(lower_bound) +
        '\n Counts of Outlyer Up: ' + str(outlyer_up) +
        '\n Counts of Outlyer Down: ' + str(outlyer_down) +
        '\n Median: ' + str(med) +
        '\n Mean: ' + str(mean) +
        '\n Number of Samples ' + str(number_samples))
        ax.boxplot(x, showbox=True, showmeans=True, showcaps=True)
        ax.set_title(boxplot_title)
        ax.set_facecolor(color_box)
        #ax.set_xlim(0, 110)
        #ax.set_ylim(-4, 4)
        #ax.grid(True)
        ax.set_xlabel(x_label)
        #ax.set_ylabel('????')

    # Definigion of axes
    fig, axs = plt.subplots(ncols=4, nrows=1, figsize=(30, 15))

    # Assignment of box plot parameters for 'Basic Time of Traffic Box Plot'
    color_box = color_list[0]
    boxplot_title = 'Basic Time of Traffic Box Plot'
    ax = axs.flat[0]
    df = pcab_query_response
    x = pcab_query_response['basic_time_diff']
    ## Drop 'NaN' from data; however it is not necessary because it has done in analysis
    x = x.dropna()
    ## Check for negative data, if there is, it means I have made a mistake
    ##  however it is not necessary because it has done in analysis
    neg = [x for x in x if x < 0]
    if len(neg) > 0:
        print('Error')
    number_samples = len(x)
    box_plot(ax, x, color_box, boxplot_title, number_samples)

    # Assignment of box plot parameters for 'Qu0eries time Box Plot'
    color_box = color_list[1]
    boxplot_title = 'Queries time Box Plot'
    ax = axs.flat[1]
    x = pcab_query_response[pcab_query_response['Info_01'] == 'Query']['basic_time_diff']
    ## Drop 'NaN' from data; however it is not necessary because it has done in analysis
    x = x.dropna()
    ## Check for negative data, if there is, it means I have made a mistake
    ## however it is not necessary because it has done in analysis
    neg = [x for x in x if x < 0]
    if len(neg) > 0:
        print('Error')
    number_samples = len(x)
    box_plot(ax, x, color_box, boxplot_title, number_samples)

    # Assignment of box plot parameters for 'Responces time Box Plot'
    color_box = color_list[2]
    boxplot_title = 'Responses time Box Plot'
    ax = axs.flat[2]
    x = pcab_query_response[pcab_query_response['Info_01'] == 'Response']['basic_time_diff']
    ## Drop 'NaN' from data; however it is not necessary because it has done in analysis
    x = x.dropna()
    ## Check for negative data, if there is, it means I have made a mistake
    ## however it is not necessary because it has done in analysis
    neg = [x for x in x if x < 0]
    if len(neg) > 0:
        print('Error')
    number_samples = len(x)
    box_plot(ax, x, color_box, boxplot_title, number_samples)

    # Assignment of box plot parameters for 'Transmission time Box Plot'
    color_box = color_list[3]
    boxplot_title = 'Transmission time Box Plot'
    ax = axs.flat[3]
    x = pcab_query_response['Response_time_diff']
    ## Drop 'NaN' from data; however it is not necessary because it has done in analysis
    x = x.dropna()
    ## Check for negative data, if there is, it means I have made a mistake
    ## however it is not necessary because it has done in analysis
    neg = [x for x in x if x < 0]
    if len(neg) > 0:
        print('Error')
    number_samples = len(x)
    box_plot(ax, x, color_box, boxplot_title, number_samples)
    print(filepath_output)
    plt.savefig(filepath_output)

filepath_output_analysis = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Analysis Results'
filepath_output_histograms = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Pcab BoxPlots'

os.chdir(r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Analysis Results')
for file_01 in glob.glob('*.csv'):
    filepath_input_help = filepath_output_analysis + '\\' + file_01
    filepath_output_help = filepath_output_histograms + '\\' + file_01[:-4] + '_boxplot.jpg'
    pcab_boxplot(filepath_input_help, filepath_output_help)