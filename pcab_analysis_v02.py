# Getting familuar with dataset
import pandas as pd
import numpy as np
import re
import warnings
import glob
import os
warnings.filterwarnings("ignore")
def pcab_analysis (filepath_input, filepath_output):

    # Importing *.csv file as a Pandas DataFram
    pcab_raw = pd.read_csv(filepath_input)

    # Extracting Features of dataset*
    #features = list(pcab_raw.columns.values)
    # Results: ['No.', 'Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info']

    # Time > 120 delete
    pcab = pcab_raw[pcab_raw['Time'] <= 120]
      
    # Finding items of 'Source' column
    source_items = list(pcab['Source'].unique())
    # Results: ['169.254.83.9', '169.254.149.247', '3Com_78:9b:01', 'Raspberr_58:67:86', 'fe80::4276:956:94c0:f49f', 'CompalIn_a0:2a:f2', '0.0.0.0', 'fe80::657f:b6ca:2f8a:5309']

    ## Declaring the regex pattern for IP addresses
    source_ip_list = []
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    for item in source_items:
        if pattern.match(item):
            source_ip_list.append(item)
    ## Results: ['169.254.83.9', '169.254.149.247', '0.0.0.0']

    # Finding items of 'Destination' column as 'Source' regarding IPs
    destination_items = list(pcab['Destination'].unique())
    destination_ip_list = []
    pattern_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    for item in destination_items:
        if pattern_ip.match(item):
            destination_ip_list.append(item)
    ## or we can:
    destination_ip = pcab.groupby(['Destination']).size().to_dict()

    # Results: ['169.254.149.247', '169.254.83.9', '255.255.255.255', '239.255.255.250']      

    # Finding items and number of 'Protocol'
    protocol_items_size = pcab.groupby(['Protocol']).size().to_dict()
    # Results: {'ARP': 127, 'DHCP': 2, 'DHCPv6': 7, 'MDNS': 5, 'Modbus/TCP': 11227, 'SSDP': 4, 'STP': 60, 'TCP': 3}

    # Calculating the average of 'Lenght' for each protocol
    protocol_items_lenghts = pcab.groupby(['Protocol']).agg({'Length':np.mean}).round(2).to_dict()
    protocol_items_lenghts = protocol_items_lenghts['Length']
    # Results: {'Length': {'ARP': 59.29, 'DHCP': 342.0, 'DHCPv6': 145.0, 'MDNS': 103.4, 'Modbus/TCP': 67.9, 'SSDP': 217.0, 'STP': 64.0, 'TCP': 62.0}}
    #for i in range(0,10):
    #    print(re.split(':',pcab.iloc[i,6])[4])

    # Add new features
    def Q_R(x):
        s = re.search('Query|Response', x)
        if s == None:
            return np.nan
        else:
            return s.group()

    def Trans(x):
        s = re.search('Trans:.*;', x)
        if s == None:
            return np.nan
        else:
            s = s.group()[8:-1]
            return int(s)


    # Finding Commands
    def Commands(x):
        s = re.search('[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]{1,}', x)
        if s == None:
            return np.nan
        else:
            s_1 = s.group()
            return s_1

    # Finding 'Read' or 'Write
    def R_W(x):
        s = re.search('[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]{1,}', x)
        if s == None:
            return np.nan
        else:
            s_1 = s.group()
            s_2 = s_1.split(' ')
            return s_2[0]

    # Finding 'Discrete' , 'Multiple' , 'Input' or 'Holding'
    def D_M_I_H(x):
        s = re.search('[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]{1,}', x)
        if s == None:
            return np.nan
        else:
            s_1 = s.group()
            s_2 = s_1.split(' ')
            return s_2[1]

    # Finding 'Inputs', 'Coils' or 'Coils'
    def I_C_R(x):
        s = re.search('[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]{1,}', x)
        if s == None:
            return np.nan
        else:
            s_1 = s.group()
            s_2 = s_1.split(' ')
            return s_2[2]

    # Assigning new columns related to anlaysis of 'Info' column and issuing new data frame
    pcab_query_response = pcab.assign(Info_01 = pcab['Info'].apply(lambda x: Q_R(x)))
    pcab_query_response = pcab_query_response.assign(Commands = pcab['Info'].apply(lambda x: Commands(x)))
    pcab_query_response = pcab_query_response.assign(Trans = pcab['Info'].apply(lambda x: Trans(x)))
    pcab_query_response = pcab_query_response.assign(R_W = pcab['Info'].apply(lambda x: R_W(x)))
    pcab_query_response = pcab_query_response.assign(D_M_I_H = pcab['Info'].apply(lambda x: D_M_I_H(x)))
    pcab_query_response = pcab_query_response.assign(I_C_R = pcab['Info'].apply(lambda x: I_C_R(x)))

    # Extracting Commands List
    Commands_Dict = pcab_query_response.groupby(['Commands']).size().to_dict()

    # Number of samples
    number_samples = len(pcab_query_response.index)
    # Results: 11435

    # It is necessary to sort data based on 'Trans' then on 'Commands'
    pcab_query_response.sort_values(['Trans','Info_01'])
    pcab_query_response = pcab_query_response.dropna(subset=['Trans'])


    # Check and omit if the first Trnas is 'Response'
    if pcab_query_response['Info_01'].head(1).values == 'Response':
        pcab_query_response.drop(pcab_query_response.head(1).index,inplace=True)

    # Basic time difference column
    ## Stablishing a list of basic time diffference to assgin to data frame
    ### Consider 1st item
    basic_time_difference = [np.nan]
    times_origin_01 = list(pcab_query_response['Time'])
    for i in range (0, len(times_origin_01)-1):
        basic_time_difference.append(times_origin_01[i+1]-times_origin_01[i])
   
    # Assigning new column for basic_time_difference
    pcab_query_response = pcab_query_response.assign(basic_time_diff = basic_time_difference)

    # Transmission time
    ## Finding 'Trans' items which are not pairs of 'Query' and 'Response'
    ### Extracting all 'Trans' items
    transactions_items = list(pcab_query_response['Trans'].unique())
    trans_no_response = []
    trans_no_query = []
    for item in transactions_items:
        if pcab_query_response[pcab_query_response['Trans'] == item]['Info_01'].shape[0] == 1:
            if list(pcab_query_response[pcab_query_response['Trans'] == item]['Info_01'])[0] == 'Query':
                trans_no_query.append(item)
            elif list(pcab_query_response[pcab_query_response['Trans'] == item]['Info_01'])[0] == 'Response':
                trans_no_response.append(item)
    ### Delete rows related of without 'Response' or 'Query'
            pcab_query_response = pcab_query_response[pcab_query_response['Trans'] != item]

    ### Extracting all 'Trans' items after omitting 
    transactions_items = list(pcab_query_response['Trans'].unique())
    ### Make a list with the same length of columns
    Time_Trans_Q_R = [np.nan]*len(pcab_query_response.index)
    ### Calculating Transmission time Response - Query, then manupulate the list and assign related column
    for i in range(0,len(transactions_items),2):
        Time_Trans_Q_R[i+1] = times_origin_01[i+1] - times_origin_01[i]
    pcab_query_response = pcab_query_response.assign(Q_R_time_diff = Time_Trans_Q_R)
    ### Make a list with the same length of columns
    times_origin_response = list(pcab_query_response[pcab_query_response['Info_01'] == 'Response']['Time'])
    Time_Trans = [np.nan]*len(pcab_query_response.index)
    ### Calculating Transmission time Response - Response, then manupulate the list and assign related column
    for i in range(0,len(transactions_items)-1):
        Time_Trans[(i+1)*2-1] = times_origin_response[i+1] - times_origin_response[i]
    pcab_query_response = pcab_query_response.assign(Response_time_diff = Time_Trans)
    # Generating txt Report
    txt_path = '\Information Summary' + filepath_input[-14:-4] + '.txt'
    ## Print information to 'txt' file
    f = open(filepath_output + txt_path,'a')
    f.write(txt_path[:-4] +
            '\nNumber of Samples: ' + str(number_samples) +
            '\n' +
            '\n............................................................' +
            '\nSource - Destination' + ' '*(35-len('Source - Destination'))+ ': ' + 'Total Number' +            '\n............................................................')
    for item in destination_ip.keys():
        f.write('\n' + str(item) + ' '*(35-len(item)) + ': ' + str(destination_ip[item]))
    f.write('\n' +
            '\n............................................................' +
            '\nProtocols' + ' '*(15-len(str('Protocols'))) + ': ' + 'Total Number' + ' '*(15-len(str('Total Number'))) + ': ' + 'Mean of Lenght' +
            '\n............................................................')
    for item in protocol_items_size.keys():
        f.write('\n' + str(item) + ' '*(15-len(item)) + ': ' + str(protocol_items_size[item]) + ' '*(15-len(str(protocol_items_size[item]))) +
        ': ' + str(protocol_items_lenghts[item]))
    f.write('\n' +
            '\n............................................................' +
            '\nCommands' + ' '*(30-len('Commands')) + ': ' + 'Total Number'
            '\n............................................................')
    for item in Commands_Dict.keys():
        f.write('\n' + str(item) + ' '*(30-len(item)) + ': ' + str(Commands_Dict[item]))
    f.write('\n' +
            '\n............................................................' +
            '\n                not rounded Transmissions' +
            '\n' +
            '\nType of Transmission' + ': Counts' + ' '*4 + ': Trans Number'
            '\n............................................................')
    
    f.write('\n' + 'Query' + ' '*(15) + ': ' + str(len(trans_no_query)) + ' '*(10-len(str(len(trans_no_query)))) + ': ') 
    for item in trans_no_query:
         f.write(str(int(item)) + ', ')
    f.write('\n' + 'Response' + ' '*(12) + ': ' + str(len(trans_no_response)) + ' '*(10-len(str(len(trans_no_response))))+ ': ')
    for item in trans_no_response:
         f.write(str(int(item)) + ', ')

    f.close()

    csv_path = filepath_output + '\Information Summary' + filepath_input[-14:-4] + '.csv'
    pcab_query_response.to_csv(csv_path)

filepath_input = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Pcab Files'
filepath_output_analysis = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Analysis Results'
os.chdir(r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Pcab Files')

for file_01 in glob.glob('*.csv'):
    filepath_input_help = filepath_input + '\\' + file_01
    pcab_analysis(filepath_input_help, filepath_output_analysis)