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
            return 'NaN'
        else:
            return s.group()

    def Trans(x):
        s = re.search('Trans:.*;', x)
        if s == None:
            return 'NaN'
        else:
            s = s.group()[8:-1]
            return int(s)


    # Finding Commands
    def Commands(x):
        s = re.search('[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]{1,}', x)
        if s == None:
            return 'NaN'
        else:
            s_1 = s.group()
            return s_1

    # Finding 'Read' or 'Write
    def R_W(x):
        s = re.search('[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]{1,}', x)
        if s == None:
            return 'NaN'
        else:
            s_1 = s.group()
            s_2 = s_1.split(' ')
            return s_2[0]

    # Finding 'Discrete' , 'Multiple' , 'Input' or 'Holding'
    def D_M_I_H(x):
        s = re.search('[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]{1,}', x)
        if s == None:
            return 'NaN'
        else:
            s_1 = s.group()
            s_2 = s_1.split(' ')
            return s_2[1]

    # Finding 'Inputs', 'Coils' or 'Coils'
    def I_C_R(x):
        s = re.search('[a-zA-Z]+ [a-zA-Z]+ [a-zA-Z]{1,}', x)
        if s == None:
            return 'NaN'
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

    # Check an omit if the first Trnas is 'Response'
    if pcab_query_response['Info_01'].head(1).values == 'Response':
        pcab_query_response.drop(pcab_query_response.head(1).index,inplace=True)
        pcab_query_response = pcab_query_response.reset_index(drop=True)
    
    # Number of samples
    number_samples = len(pcab_query_response.index)
    # Results: 11435

    # in order to have precise calculation number of 'Query' and 'Response' has to be equal
    '''while len(pcab_query_response[pcab_query_response['Info_01'] == 'Query']) != len(pcab_query_response[pcab_query_response['Info_01'] == 'Response']):
        pcab_query_response.drop(pcab_query_response.tail(1).index,inplace=True)'''

    # Extracting Commands List
    Commands_Dict = pcab_query_response.groupby(['Commands']).size().to_dict()

    # Basic time difference column
    ## Stablishing a list of basic time diffference to assgin to data frame
    ### Consider 1st item
    basic_time_difference = []

    for i in range (0, number_samples-1):
        basic_time_difference.append(pcab_query_response.loc[i+1,'Time']-pcab_query_response.loc[i,'Time'])
    ### consider last item
    basic_time_difference.append('NaN')

    # Transmission time
    ## Stablishing a list of Transmission time to assgin to data frame
    ### Consider 1st item
    transactions_items = list(pcab_query_response['Trans'].unique())
    transactions_items = [x for x in transactions_items if str(x) != 'NaN']
    pcab_query_response.assign(Time_Trans = ['NaN']*len(pcab_query_response.index))
    pcab_query_response.reset_index(drop=True, inplace=True)
    for i in range(0,len(transactions_items)-1):
        item = transactions_items[i]
        t01 = pcab_query_response[(pcab_query_response['Info_01'] == 'Response') & (pcab_query_response['Trans'] == item + 1)]['Time'].values
        t02 = pcab_query_response[(pcab_query_response['Info_01'] == 'Response') & (pcab_query_response['Trans'] == item)]['Time'].values
        print(t01[0])
        print(t02[0])
        print(item)
        print('-----------')
        pcab_query_response[(pcab_query_response['Info_01'] == 'Response') & (pcab_query_response['Trans'] == item + 1)]['Time_Trans'] = t01[0] - t02[0]

    # Assigning new column for basic_time_difference
    pcab_query_response = pcab_query_response.assign(Time_diff = basic_time_difference)

    txt_path = '\Information Summary' + filepath_input[-14:-4] + '.txt'
    # Print information to 'txt' file
    f = open(filepath_output + txt_path,'a')
    f.write(txt_path[:-4] +
            '\nNumber of Samples: ' + str(number_samples) +
            '\n' +
            '\n............................................................' +
            '\n                   Source - Destination' +
            '\n............................................................')
    for item in destination_ip.keys():
        f.write('\n' + str(item) + ' '*(35-len(item)) + ': ' + str(destination_ip[item]))
    f.write('\n' +
            '\n............................................................' +
            '\n Protocols, Total Number of them and their Average Lenghts' +
            '\n............................................................')
    for item in protocol_items_size.keys():
        f.write('\n' + str(item) + ' '*(15-len(item)) + ': ' + str(protocol_items_size[item]) + ' '*(10-len(str(protocol_items_size[item]))) +
        ': ' + str(protocol_items_lenghts[item]))
    f.write('\n' +
            '\n............................................................' +
            '\n                        Commands' +
            '\n............................................................')
    for item in Commands_Dict.keys():
        f.write('\n' + str(item) + ' '*(30-len(item)) + ': ' + str(Commands_Dict[item]))
    f.close()

    csv_path = filepath_output + '\Information Summary' + filepath_input[-14:-4] + '.csv'
    pcab_query_response.to_csv(csv_path)

filepath_input = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Pcab Files'
filepath_output_analysis = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Analysis Results'
os.chdir(r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\Pcab Files')

for file_01 in glob.glob('*.csv'):
    filepath_input_help = filepath_input + '\\' + file_01
    pcab_analysis(filepath_input_help, filepath_output_analysis)