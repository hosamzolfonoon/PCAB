# Getting familuar with dataset
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import numpy as np

def pcab_boxplot (filepath_input, filepath_output):
    print(filepath_input)
    # Read data frame
    pcab_query_response = pd.read_csv(filepath_input)

    # Definition color lists
    color_list = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']

    # Adjusting font size
    plt.rcParams.update({'font.size': 16})

    # Box Plotn function
    def box_plot(ax, df, boxplot_title):
        df.plot(ax = ax, kind = 'box', title = boxplot_title, fontsize = 12, rot = 45)

    # Definigion of axes
    fig, axs = plt.subplots(ncols=3, nrows=1, figsize=(30, 15))
    pcab_query_response = pd.read_csv(filepath_input)
    columns_commands = list(pcab_query_response['Commands'].unique())
    # Assignment of box plot parameters for 'Basic Time of Traffic Box Plot'
    color_box = color_list[0]
    boxplot_title = 'Basic Time of Traffic Box Plot'
    ax = axs.flat[0]
    df_0 = pd.DataFrame(columns = columns_commands)
    for i in range(0, len(columns_commands)):
        list_help = []
        list_help = list(pcab_query_response[pcab_query_response['Commands'] == columns_commands[i]]['basic_time_diff'])
        list_help_nan = []
        if len(list_help) < len(df_0.index):
            list_help_nan = [np.nan]*(len(df_0.index) - len(list_help))
            for item_list_help in list_help_nan:
                list_help.append(item_list_help)
        else:
            list_help_nan = [np.nan]*(len(list_help) - len(df_0.index))
            for item_list_help in list_help_nan:
                list_help.append(item_list_help)

        df_0[columns_commands[i]] = list_help
    box_plot(ax, df_0, boxplot_title)

    # Assignment of box plot parameters for 'Basic Time of Traffic Box Plot'
    color_box = color_list[1]
    boxplot_title = 'R_R Transmission time Box Plot'
    ax = axs.flat[1]
    df_1 = pd.DataFrame(columns = columns_commands)
    for i in range(0, len(columns_commands)):
        list_help = []
        list_help = list(pcab_query_response[pcab_query_response['Commands'] == columns_commands[i]]['Response_time_diff'])
        list_help_nan = []
        if len(list_help) < len(df_1.index):
            list_help_nan = [np.nan]*(len(df_1.index) - len(list_help))
            for item_list_help in list_help_nan:
                list_help.append(item_list_help)
        else:
            list_help_nan = [np.nan]*(len(list_help) - len(df_1.index))
            for item_list_help in list_help_nan:
                list_help.append(item_list_help)

        df_1[columns_commands[i]] = list_help
    box_plot(ax, df_1, boxplot_title)

    # Assignment of box plot parameters for 'Basic Time of Traffic Box Plot'
    color_box = color_list[2]
    boxplot_title = 'Q_R Transmission time Box Plot'
    ax = axs.flat[2]
    df_2 = pd.DataFrame(columns = columns_commands)
    for i in range(0, len(columns_commands)):
        list_help = []
        list_help = list(pcab_query_response[pcab_query_response['Commands'] == columns_commands[i]]['Q_R_time_diff'])
        
        if len(list_help) < len(df_2.index):
            list_help_nan = [np.nan]*(len(df_2.index) - len(list_help))
            for item_list_help in list_help_nan:
                list_help.append(item_list_help)
        elif len(list_help) > len(df_2.index):
            list_help_nan = [np.nan]*(len(list_help) - len(df_2.index))
            for item_list_help in list_help_nan:
                list_help.append(item_list_help)

        df_2[columns_commands[i]] = list_help
    box_plot(ax, df_2, boxplot_title)
    print(filepath_output)
    plt.savefig(filepath_output)




filepath_output_analysis = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Analysis Results'
filepath_output_histograms = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Pcab Commands BoxPlots'

os.chdir(r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Analysis Results')
for file_01 in glob.glob('*.csv'):
    filepath_input_help = filepath_output_analysis + '\\' + file_01
    filepath_output_help = filepath_output_histograms + '\\' + file_01[:-4] + '_commands_boxplot.jpg'
    pcab_boxplot(filepath_input_help, filepath_output_help)